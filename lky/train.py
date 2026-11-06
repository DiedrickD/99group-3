"""Small reproducible LoRA experiment with assistant-only loss and source-held-out validation."""
import argparse
import json
import math
import random
import time
from datetime import datetime, timezone
from pathlib import Path
from .data import ROOT, read_jsonl, write_json, digest, load_notes
from .prompt import messages_for


def main():
    import torch
    from transformers import AutoModelForCausalLM, AutoTokenizer
    from peft import LoraConfig, get_peft_model
    from .generator import model_location
    parser = argparse.ArgumentParser()
    parser.add_argument("--epochs", type=int, default=2)
    parser.add_argument("--lr", type=float, default=2e-4)
    parser.add_argument("--max-length", type=int, default=384)
    parser.add_argument("--accumulation", type=int, default=4)
    parser.add_argument("--threads", type=int, default=4)
    parser.add_argument("--output", default=str(ROOT / "models/lky-lora"))
    args = parser.parse_args()
    if min(args.epochs, args.max_length, args.accumulation, args.threads) < 1:
        parser.error("epochs, max-length, accumulation and threads must be positive")
    torch.set_num_threads(args.threads)
    torch.manual_seed(42)
    random.seed(42)
    config = json.loads((ROOT / "config/model.json").read_text(encoding="utf-8"))
    device = "cuda" if torch.cuda.is_available() else "cpu"
    dtype = torch.float32 if device == "cpu" else torch.float16
    location = model_location(config)
    tokenizer = AutoTokenizer.from_pretrained(location)
    model = AutoModelForCausalLM.from_pretrained(location,
                                               torch_dtype=dtype, attn_implementation="sdpa").to(device)
    model.name_or_path = config["model_id"]
    model.config._name_or_path = config["model_id"]
    model.config.use_cache = False
    model = get_peft_model(model, LoraConfig(r=8, lora_alpha=16, lora_dropout=0.05,
                                             target_modules=["q_proj", "v_proj"], task_type="CAUSAL_LM", bias="none"))
    model.peft_config["default"].base_model_name_or_path = config["model_id"]
    model.peft_config["default"].revision = config["revision"]
    trainable, total = model.get_nb_trainable_parameters()
    note_map = {n["note_id"]: n for n in load_notes()}
    train = read_jsonl(ROOT / "data/train.jsonl")
    validation = read_jsonl(ROOT / "data/validation.jsonl")
    assert not ({s for r in train for s in r["source_ids"]} & {s for r in validation for s in r["source_ids"]})

    def encode(row):
        messages = messages_for(row["question"], [note_map[nid] for nid in row["note_ids"]])
        prompt = tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)
        prefix = tokenizer.encode(prompt, add_special_tokens=False)
        answer = tokenizer.encode(row["answer"] + tokenizer.eos_token, add_special_tokens=False)
        if len(prefix) + len(answer) > args.max_length:
            raise ValueError(f'{row["id"]}: sequence exceeds max-length; increase it instead of silently losing labels')
        ids = prefix + answer
        return {"input_ids": torch.tensor([ids], device=device),
                "attention_mask": torch.ones((1, len(ids)), dtype=torch.long, device=device),
                "labels": torch.tensor([[-100] * len(prefix) + answer], device=device)}

    encoded_train = [encode(row) for row in train]
    encoded_validation = [encode(row) for row in validation]

    def validation_loss():
        model.eval()
        numerator, denominator = 0.0, 0
        with torch.no_grad():
            for batch in encoded_validation:
                count = int((batch["labels"][:, 1:] != -100).sum())
                numerator += model(**batch).loss.item() * count
                denominator += count
        return numerator / denominator

    started = time.perf_counter()
    before = validation_loss()
    optimizer = torch.optim.AdamW((p for p in model.parameters() if p.requires_grad), lr=args.lr)
    scaler = torch.amp.GradScaler("cuda", enabled=device == "cuda")
    logs, steps = [], 0
    optimizer.zero_grad(set_to_none=True)
    print(f"device={device}; trainable={trainable:,}/{total:,}; held-out loss before={before:.5f}", flush=True)
    for epoch in range(args.epochs):
        model.train()
        order = list(range(len(encoded_train)))
        random.shuffle(order)
        losses = []
        for offset, index in enumerate(order):
            loss = model(**encoded_train[index]).loss
            losses.append(loss.detach().float().item())
            if not math.isfinite(losses[-1]):
                raise RuntimeError("Non-finite loss; no adapter was saved")
            # Correct scaling for the last, potentially shorter accumulation group.
            group_size = min(args.accumulation, len(order) - (offset // args.accumulation) * args.accumulation)
            scaler.scale(loss / group_size).backward()
            if (offset + 1) % args.accumulation == 0 or offset == len(order) - 1:
                scaler.unscale_(optimizer)
                torch.nn.utils.clip_grad_norm_(model.parameters(), 1.0)
                scaler.step(optimizer)
                scaler.update()
                optimizer.zero_grad(set_to_none=True)
                steps += 1
                print(f"epoch={epoch+1} optimizer_step={steps} mean_loss={sum(losses)/len(losses):.5f}", flush=True)
        logs.append({"epoch": epoch+1, "mean_example_training_loss": sum(losses)/len(losses),
                     "validation_token_loss": validation_loss()})
    after = validation_loss()
    model.save_pretrained(args.output, safe_serialization=True)
    # The unchanged tokenizer is loaded from the pinned base model at inference.
    report = {"completed_utc": datetime.now(timezone.utc).isoformat(), "base_model": config,
              "device": device, "torch_version": torch.__version__, "seed": 42,
              "epochs": args.epochs, "optimizer_steps": steps, "learning_rate": args.lr,
              "micro_batch_size": 1, "gradient_accumulation": args.accumulation,
              "max_length": args.max_length, "lora": {"r": 8, "alpha": 16, "dropout": 0.05, "targets": ["q_proj", "v_proj"]},
              "trainable_parameters": trainable, "total_parameters_including_adapter": total,
              "train_examples": len(train), "validation_examples": len(validation),
              "training_data_sha256": digest(ROOT / "data/train.jsonl"),
              "validation_data_sha256": digest(ROOT / "data/validation.jsonl"),
              "validation_loss_before": before, "validation_loss_after": after,
              "elapsed_seconds": round(time.perf_counter() - started, 2), "epochs_log": logs,
              "interpretation": "Small feasibility experiment. Loss does not establish historical accuracy, persona quality, or improvement in chatbot answers."}
    write_json(ROOT / "reports/training.json", report)
    write_json(Path(args.output) / "run.json", report)
    if Path(args.output).resolve() == (ROOT / "models/lky-lora").resolve():
        write_json(ROOT / "models/manifest.json", {
            "adapter_file": "models/lky-lora/adapter_model.safetensors",
            "sha256": digest(Path(args.output) / "adapter_model.safetensors"),
            "base_model": config, "training_data_sha256": report["training_data_sha256"]})
    print(json.dumps(report, indent=2), flush=True)


if __name__ == "__main__":
    main()
