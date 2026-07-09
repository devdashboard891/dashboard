import json, os

notebook = {
 "cells": [
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "# Fine-tune Qwen2.5-Coder-1.5B \u2014 \u0420\u0443\u0441\u0441\u043a\u0438\u0439 \u0443\u0447\u0438\u0442\u0435\u043b\u044c \u043a\u043e\u0434\u0430\n",
    "\u041d\u0430\u0436\u043c\u0438 **Runtime \u2192 Run all** (\u0441\u043d\u0430\u0447\u0430\u043b\u0430 **Runtime \u2192 Change runtime type \u2192 T4 GPU**)\n",
    "\u0414\u0430\u0442\u0430\u0441\u0435\u0442 \u0437\u0430\u0433\u0440\u0443\u0436\u0430\u0435\u0442\u0441\u044f \u0441 GitHub."
   ]
  },
  {
   "cell_type": "code",
   "metadata": {},
   "source": [
    "!pip install -q torch transformers accelerate peft bitsandbytes trl unsloth\n",
    "import os; os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'"
   ],
   "execution_count": None,
   "outputs": []
  },
  {
   "cell_type": "code",
   "metadata": {},
   "source": [
    "import json, random, urllib.request\n",
    "url = 'https://raw.githubusercontent.com/devdashboard891/dashboard/refs/heads/main/training_data/code_tutor_dataset.json'\n",
    "with urllib.request.urlopen(url) as f:\n",
    "    data = json.loads(f.read().decode('utf-8'))\n",
    "random.shuffle(data)\n",
    "print(f'\u0417\u0430\u0433\u0440\u0443\u0436\u0435\u043d\u043e {len(data)} \u043f\u0440\u0438\u043c\u0435\u0440\u043e\u0432')"
   ],
   "execution_count": None,
   "outputs": []
  },
  {
   "cell_type": "code",
   "metadata": {},
   "source": [
    "def fmt(ex):\n",
    "    s = '\u0422\u044b \u2014 \u043e\u043f\u044b\u0442\u043d\u044b\u0439 \u0443\u0447\u0438\u0442\u0435\u043b\u044c \u043f\u0440\u043e\u0433\u0440\u0430\u043c\u043c\u0438\u0440\u043e\u0432\u0430\u043d\u0438\u044f. \u041e\u0442\u0432\u0435\u0447\u0430\u0435\u0448\u044c \u043d\u0430 \u0440\u0443\u0441\u0441\u043a\u043e\u043c, \u0441 \u043f\u0440\u0438\u043c\u0435\u0440\u0430\u043c\u0438 \u043a\u043e\u0434\u0430.'\n",
    "    u = ex['instruction']\n",
    "    if ex.get('input'): u += '\\n' + ex['input']\n",
    "    return {'text': f\"<|im_start|>system\\n{s}<|im_end|>\\n<|im_start|>user\\n{u}<|im_end|>\\n<|im_start|>assistant\\n{ex['output']}<|im_end|>\"}\n",
    "formatted = [fmt(ex) for ex in data]"
   ],
   "execution_count": None,
   "outputs": []
  },
  {
   "cell_type": "code",
   "metadata": {},
   "source": [
    "from unsloth import FastLanguageModel\n",
    "import torch\n",
    "model, tokenizer = FastLanguageModel.from_pretrained(\n",
    "    model_name='Qwen/Qwen2.5-Coder-1.5B-Instruct',\n",
    "    max_seq_length=2048, dtype=torch.bfloat16, load_in_4bit=True,\n",
    ")\n",
    "print('\u041c\u043e\u0434\u0435\u043b\u044c \u0437\u0430\u0433\u0440\u0443\u0436\u0435\u043d\u0430')"
   ],
   "execution_count": None,
   "outputs": []
  },
  {
   "cell_type": "code",
   "metadata": {},
   "source": [
    "model = FastLanguageModel.get_peft_model(\n",
    "    model, r=16, lora_alpha=32, lora_dropout=0,\n",
    "    target_modules=['q_proj','k_proj','v_proj','o_proj',\n",
    "                    'gate_proj','up_proj','down_proj'],\n",
    "    use_rslora=True,\n",
    ")\n",
    "print(f'Trainable: {model.num_parameters(only_trainable=True):,}')"
   ],
   "execution_count": None,
   "outputs": []
  },
  {
   "cell_type": "code",
   "metadata": {},
   "source": [
    "import datasets\n",
    "def tok(ex): return tokenizer(ex['text'], truncation=True, max_length=2048)\n",
    "ds = datasets.Dataset.from_list(formatted).map(tok, batched=False)\n",
    "print(f'\u041f\u0440\u0438\u043c\u0435\u0440\u043e\u0432: {len(ds)}')"
   ],
   "execution_count": None,
   "outputs": []
  },
  {
   "cell_type": "code",
   "metadata": {},
   "source": [
    "from trl import SFTTrainer\n",
    "from transformers import TrainingArguments\n",
    "trainer = SFTTrainer(\n",
    "    model=model, tokenizer=tokenizer, train_dataset=ds,\n",
    "    args=TrainingArguments(\n",
    "        output_dir='/content/qwen-coder-finetuned',\n",
    "        per_device_train_batch_size=2,\n",
    "        gradient_accumulation_steps=4,\n",
    "        num_train_epochs=3, learning_rate=2e-4,\n",
    "        bf16=True, logging_steps=10, save_steps=100,\n",
    "        save_total_limit=2, remove_unused_columns=False,\n",
    "        report_to='none',\n",
    "    ),\n",
    ")\n",
    "trainer.train()\n",
    "print('\u041e\u0431\u0443\u0447\u0435\u043d\u0438\u0435 \u0437\u0430\u0432\u0435\u0440\u0448\u0435\u043d\u043e')"
   ],
   "execution_count": None,
   "outputs": []
  },
  {
   "cell_type": "code",
   "metadata": {},
   "source": [
    "model.save_pretrained('/content/qwen-coder-lora')\n",
    "tokenizer.save_pretrained('/content/qwen-coder-lora')\n",
    "print('LoRA \u0441\u043e\u0445\u0440\u0430\u043d\u0435\u043d\u0430')"
   ],
   "execution_count": None,
   "outputs": []
  },
  {
   "cell_type": "code",
   "metadata": {},
   "source": [
    "from peft import PeftModel\n",
    "base, _ = FastLanguageModel.from_pretrained(\n",
    "    'Qwen/Qwen2.5-Coder-1.5B-Instruct',\n",
    "    load_in_4bit=False, dtype=torch.bfloat16,\n",
    ")\n",
    "lora = PeftModel.from_pretrained(base, '/content/qwen-coder-lora')\n",
    "merged = lora.merge_and_unload()\n",
    "merged.save_pretrained('/content/qwen-coder-merged')\n",
    "tokenizer.save_pretrained('/content/qwen-coder-merged')\n",
    "print('\u041c\u043e\u0434\u0435\u043b\u044c \u043e\u0431\u044a\u0435\u0434\u0438\u043d\u0435\u043d\u0430')"
   ],
   "execution_count": None,
   "outputs": []
  },
  {
   "cell_type": "code",
   "metadata": {},
   "source": [
    "if not os.path.exists('/content/llama.cpp'):\n",
    "    !git clone --depth 1 https://github.com/ggerganov/llama.cpp.git /content/llama.cpp\n",
    "!python /content/llama.cpp/convert_hf_to_gguf.py \\\n",
    "    /content/qwen-coder-merged \\\n",
    "    --outfile /content/qwen-coder-russian.gguf \\\n",
    "    --outtype q4_k_m\n",
    "import shutil\n",
    "shutil.make_archive('/content/qwen-coder', 'zip', '/content', 'qwen-coder-russian.gguf')\n",
    "sz2 = os.path.getsize('/content/qwen-coder-russian.gguf')\n",
    "print(f'GGUF: {sz2 / 1024**2:.0f} MB')"
   ],
   "execution_count": None,
   "outputs": []
  },
  {
   "cell_type": "code",
   "metadata": {},
   "source": [
    "from google.colab import files\n",
    "files.download('/content/qwen-coder.zip')\n",
    "print('\u0413\u043e\u0442\u043e\u0432\u043e! \u0420\u0430\u0441\u043f\u0430\u043a\u0443\u0439 .gguf, \u0437\u0430\u043f\u0443\u0441\u0442\u0438 llama-server')"
   ],
   "execution_count": None,
   "outputs": []
  }
 ],
 "metadata": {
  "accelerator": "GPU",
  "colab": {"provenance": [], "gpuType": "T4"},
  "kernelspec": {"display_name": "Python 3", "name": "python3"},
  "language_info": {"name": "python"}
 },
 "nbformat": 4,
 "nbformat_minor": 0
}

with open('finetune_colab.ipynb', 'w') as f:
    json.dump(notebook, f, ensure_ascii=False, indent=1)

sz = os.path.getsize('finetune_colab.ipynb')
print(f'OK: {sz / 1024:.0f} KB')
