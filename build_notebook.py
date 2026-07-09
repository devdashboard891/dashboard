import json, base64, os

with open('training_data/code_tutor_dataset.json') as f:
    dataset = json.load(f)

encoded = base64.b64encode(
    json.dumps(dataset, ensure_ascii=False).encode('utf-8')
).decode('ascii')

notebook = {
 "cells": [
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "# Fine-tune Qwen2.5-Coder-1.5B — Русский учитель кода\n",
    "Датасет встроен (base64). Нажми **Runtime → Run all**\n",
    "Нужен GPU: **Runtime → Change runtime type → T4 GPU**"
   ]
  },
  {
   "cell_type": "code",
   "metadata": {},
   "source": [
    "!pip install -q torch transformers accelerate peft bitsandbytes trl unsloth\n",
    "!CMAKE_ARGS=\"-DLLAMA_CUDA=on\" pip install -q llama-cpp-python 2>/dev/null || true\n",
    "import os; os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'"
   ],
   "execution_count": None,
   "outputs": []
  },
  {
   "cell_type": "code",
   "metadata": {},
   "source": [
    "import json, base64, random\n",
    "encoded = '" + encoded + "'\n",
    "data = json.loads(base64.b64decode(encoded).decode('utf-8'))\n",
    "random.shuffle(data)\n",
    "print(f'Загружено {len(data)} примеров')"
   ],
   "execution_count": None,
   "outputs": []
  },
  {
   "cell_type": "code",
   "metadata": {},
   "source": [
    "def fmt(ex):\n",
    "    s = 'Ты — опытный учитель программирования. Отвечаешь на русском, с примерами кода.'\n",
    "    u = ex['instruction']\n",
    "    if ex.get('input'): u += '\\n' + ex['input']\n",
    "    return {'text': f\"<|im_start|>system\\n{s}<|im_end|>\\n<|im_start|>user\\n{u}<|im_end|>\\n<|im_start|>assistant\\n{ex['output']}<|im_end|>\"}\n",
    "formatted = [fmt(ex) for ex in data]\n",
    "print(formatted[0]['text'][:120])"
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
    "print('Модель загружена')"
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
    "print(f'Примеров: {len(ds)}')"
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
    "print('Обучение завершено')"
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
    "print('LoRA сохранена')"
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
    "print('Модель объединена')"
   ],
   "execution_count": None,
   "outputs": []
  },
  {
   "cell_type": "code",
   "metadata": {},
   "source": [
    "import os\n",
    "if not os.path.exists('/content/llama.cpp'):\n",
    "    !git clone --depth 1 https://github.com/ggerganov/llama.cpp.git /content/llama.cpp\n",
    "!pip install -q /content/llama.cpp 2>/dev/null || true\n",
    "!python /content/llama.cpp/convert_hf_to_gguf.py \\\n",
    "    /content/qwen-coder-merged \\\n",
    "    --outfile /content/qwen-coder-russian.gguf \\\n",
    "    --outtype q4_k_m\n",
    "print(f'GGUF: {os.path.getsize(\"/content/qwen-coder-russian.gguf\") / 1024**2:.0f} MB')\n",
    "import shutil\n",
    "shutil.make_archive('/content/qwen-coder', 'zip', '/content', 'qwen-coder-russian.gguf')"
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
    "print('Готово! Распакуй .gguf, запусти llama-server')"
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
    json.dump(notebook, f, ensure_ascii=False)

size = os.path.getsize('finetune_colab.ipynb')
data_len = len(dataset)
print(f'OK: {size/1024:.0f} KB, {data_len} examples')
