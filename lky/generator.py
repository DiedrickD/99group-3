from pathlib import Path
from .data import ROOT

BASE_MODEL = "Qwen/Qwen2.5-0.5B-Instruct"
# Resolve the exact model commit during preparation; saved in config/model.json.


def model_location(config):
    from huggingface_hub import snapshot_download
    directory = ROOT / config.get("local_directory", "models/base/" + config["model_id"].replace("/", "--"))
    if not (directory / "config.json").exists() or not list(directory.glob("*.safetensors")):
        snapshot_download(config["model_id"], revision=config["revision"], local_dir=directory,
                          allow_patterns=["*.json", "*.safetensors", "*.txt", "*.model", "*.tiktoken"])
    return str(directory)


class LocalGenerator:
    def __init__(self, adapter=None, max_new_tokens=180, threads=4):
        import json
        import torch
        from transformers import AutoModelForCausalLM, AutoTokenizer
        config = json.loads((ROOT / "config/model.json").read_text(encoding="utf-8"))
        location = model_location(config)
        torch.set_num_threads(threads)
        self.torch = torch
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.max_new_tokens = max_new_tokens
        self.tokenizer = AutoTokenizer.from_pretrained(location)
        self.model = AutoModelForCausalLM.from_pretrained(
            location, torch_dtype=torch.float16 if self.device == "cuda" else torch.float32,
            attn_implementation="sdpa").to(self.device)
        if adapter:
            from peft import PeftModel
            adapter_config = json.loads((Path(adapter) / "adapter_config.json").read_text(encoding="utf-8"))
            if (adapter_config["base_model_name_or_path"] != config["model_id"]
                    or adapter_config.get("revision") != config["revision"]):
                raise ValueError("Adapter and configured base model revisions differ; prepare and train the same model.")
            self.model = PeftModel.from_pretrained(self.model, str(Path(adapter)))
        self.model.eval()

    def generate(self, messages):
        text = self.tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)
        encoded = self.tokenizer(text, return_tensors="pt").to(self.device)
        with self.torch.inference_mode():
            output = self.model.generate(**encoded, max_new_tokens=self.max_new_tokens,
                                         do_sample=False, repetition_penalty=1.08,
                                         pad_token_id=self.tokenizer.eos_token_id)
        return self.tokenizer.decode(output[0, encoded.input_ids.shape[1]:], skip_special_tokens=True).strip()
