import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def main():
    def cell(kind, text):
        result = {"cell_type": kind, "metadata": {}, "source": text.splitlines(keepends=True)}
        if kind == "code":
            result.update(execution_count=None, outputs=[])
        return result
    notebook = {"nbformat": 4, "nbformat_minor": 5,
                "metadata": {"kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"},
                             "colab": {"name": "Lee Kuan Yew: LoRA + RAG + Eval", "provenance": []}},
                "cells": [
        cell("markdown", "# Source-grounded Lee Kuan Yew simulation\nSelect **Runtime > Change runtime type > T4 GPU**, then run cells in order. No API key or Drive mount is required for this public-repository workflow. This notebook is an unexecuted workflow template; executed local results are in the repository. A GPU allocation is subject to your Colab quota.\n"),
        cell("code", "import os, pathlib, subprocess, sys\nimport torch\nassert torch.cuda.is_available(), 'Select a GPU runtime before training, or use the local CPU instructions.'\nprint(torch.cuda.get_device_name(0))\nworkspace = pathlib.Path('/content/99task_lee_kuan_yew_llm')\nif not workspace.exists():\n    subprocess.run(['git', 'clone', 'https://github.com/DiedrickD/99group-3.git', str(workspace)], check=True)\nos.chdir(workspace)\nsubprocess.run(['git', 'rev-parse', 'HEAD'], check=True)\nsubprocess.run([sys.executable, '-m', 'pip', 'install', '-q', '-r', 'requirements-colab.txt'], check=True)\n"),
        cell("markdown", "## Choose a model\nKeep 0.5B to reproduce the small experiment. Change to `Qwen/Qwen2.5-1.5B-Instruct` for a larger experiment; rerun preparation, training and evaluation together. Do not compare results across model sizes as if only the adapter changed. The exact model commit is recorded automatically.\n"),
        cell("code", "MODEL_ID = 'Qwen/Qwen2.5-0.5B-Instruct'\ndef run(*args):\n    subprocess.run([sys.executable, *args], check=True)\nrun('scripts/validate_data.py')\nrun('scripts/prepare_model.py', '--model-id', MODEL_ID)\nrun('-m', 'lky.train', '--epochs', '2')\n"),
        cell("code", "run('-m', 'lky.evaluate', '--backend', 'notes', '--output', 'reports/colab-notes.json')\nrun('-m', 'lky.evaluate', '--backend', 'base', '--output', 'reports/colab-base-rag.json')\nrun('-m', 'lky.evaluate', '--backend', 'lora', '--output', 'reports/colab-lora-rag.json')\nrun('-m', 'lky.evaluate', '--backend', 'base', '--no-rag', '--output', 'reports/colab-base-no-rag.json')\nrun('-m', 'lky.evaluate', '--backend', 'lora', '--no-rag', '--output', 'reports/colab-lora-no-rag.json')\n"),
        cell("code", "# Download the trained adapter and measured reports before the runtime expires.\nimport zipfile\nfrom google.colab import files\narchive = '/content/lky-training-artifacts.zip'\nwith zipfile.ZipFile(archive, 'w', zipfile.ZIP_DEFLATED) as output:\n    for folder in ['models/lky-lora', 'reports', 'config']:\n        for path in pathlib.Path(folder).rglob('*'):\n            if path.is_file():\n                output.write(path, path.as_posix())\nfiles.download(archive)\n"),
        cell("markdown", "## Temporary chat demo\nThe next cell creates a public Gradio share URL. It works only while this runtime and server remain available. Use the repository chat examples as the permanent submission link. Each turn is independent.\n"),
        cell("code", "from app import build_app\ndemo = build_app('lora')\ndemo.launch(share=True, debug=False)\n"),
    ]}
    # Jupyter may keep an absolute initial working directory in sys.path.
    for item in notebook["cells"]:
        if item["cell_type"] == "code" and any("os.chdir(workspace)" in line for line in item["source"]):
            index = next(i for i, line in enumerate(item["source"]) if "os.chdir(workspace)" in line)
            item["source"].insert(index + 1, "sys.path.insert(0, str(workspace))\n")
    folder = ROOT / "notebooks"
    folder.mkdir(exist_ok=True)
    (folder / "train_colab.ipynb").write_text(json.dumps(notebook, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
