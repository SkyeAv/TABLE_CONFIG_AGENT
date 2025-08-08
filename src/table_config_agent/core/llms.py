from src.table_config_agent.chroma_db.template_examples import (
    TEMPLATE_EXAMPLES,
    Example,
)
from transformers import AutoTokenizer, AutoModel, AutoModelForCausalLM
from peft import get_peft_model, LoraConfig, TaskType, PeftModel
from transformers import Trainer, TrainingArguments
from contextlib import contextmanager
from typing import ContextManager
from datasets import Dataset
from pathlib import Path
from typing import Any
from tqdm import tqdm
import numpy as np
import random
import torch


def set_seed(seed: int) -> None:
    torch.manual_seed(seed)
    np.random.seed(seed)
    random.seed(seed)
    return None


@contextmanager  # type: ignore
def suppress_tqdm() -> ContextManager:  # type: ignore
    original_init = tqdm.__init__

    def patched_init(self, *args, **kwargs) -> None:  # type: ignore
        kwargs["disable"] = True
        original_init(self, *args, **kwargs)
        return None

    tqdm.__init__ = patched_init
    try:
        yield
    finally:
        tqdm.__init__ = original_init


def tokenize_and_mask(
    tokenizer: AutoTokenizer, batch: dict[str, Any], sep: str, max_length: int
) -> dict[str, Any]:
    texts: list[str] = [p + sep + t for p, t in zip(batch["prompt"], batch["target"])]
    tokens = tokenizer(
        texts, truncation=True, padding="max_length", max_length=max_length
    )
    labels = tokens["input_ids"].copy()
    for i, pid in enumerate(
        tokenizer(
            batch["prompt"],
            truncation=True,
            padding="max_length",
            max_length=max_length,
        )["input_ids"]
    ):
        prompt_len: int = sum(1 for token in pid if token != tokenizer.pad_token_id)
        labels[i][:prompt_len] = -100  # ignore prompt tokens in loss
        tokens["labels"] = labels
        return tokens


def train_dataset(tokenizer: AutoTokenizer, max_length: int = 512) -> Dataset:
    sep: str = tokenizer.eos_token or tokenizer.sep_token or ""
    examples: list[Example] = TEMPLATE_EXAMPLES
    ds = Dataset.from_dict(
        {
            "prompt": [ex["input"] for ex in examples],
            "target": [ex["output"] for ex in examples],
        }
    )
    return ds.map(
        (lambda x: tokenize_and_mask(tokenizer, x, sep, max_length)),
        batched=True,
        remove_columns=["prompt", "target"],
    ).set_format("torch", columns=["input_ids", "attention_mask", "labels"])


def finetune(
    tokenizer: AutoTokenizer,
    pipeline_model: AutoModelForCausalLM,
    posix_model_path: str,
) -> AutoModelForCausalLM:
    lora = LoraConfig(
        task_type=TaskType.CAUSAL_LM,
        inference_mode=False,
        r=8,
        lora_alpha=16,
        lora_dropout=0.05,
    )
    pipeline_pfet = get_peft_model(pipeline_model, lora)
    args = TrainingArguments(
        output_dir=posix_model_path,
        overwrite_output_dir=True,
        num_train_epochs=3,
        learning_rate=1e-4,
        weight_decay=0.01,
        logging_strategy="no",
    )
    trainer = Trainer(
        model=pipeline_pfet, args=args, train_dataset=train_dataset(tokenizer)
    )
    trainer.train()
    pipeline_pfet.save_pretrained(posix_model_path)
    return pipeline_pfet


def from_transformers(
    hf_model: str, offload_folder: Path, lora_pipeline_path: Path
) -> tuple[AutoTokenizer, AutoModel, AutoModelForCausalLM]:
    with suppress_tqdm():
        try:
            tokenizer = AutoTokenizer.from_pretrained(hf_model, use_fast=True)  # type: ignore
            _ = tokenizer.tokenize("Hai")  # Force backend check
        except Exception:
            tokenizer = AutoTokenizer.from_pretrained(hf_model, use_fast=False)  # type: ignore
        embeding_model = AutoModel.from_pretrained(
            hf_model,
            device_map={"": "cpu"},
            torch_dtype="float32",
            low_cpu_mem_usage=False,
        ).eval()
        pipeline_model = AutoModelForCausalLM.from_pretrained(
            hf_model,
            device_map="auto",
            torch_dtype="float16",
            offload_folder=offload_folder.as_posix(),
            offload_state_dict=True,
            low_cpu_mem_usage=True,
        )
        if lora_pipeline_path.exists():
            pipeline_model = PeftModel.from_pretrained(
                pipeline_model,
                lora_pipeline_path.as_posix(),
                device_map="auto",
                torch_dtype="float16",
                offload_folder=offload_folder.as_posix(),
            )
        else:
            pipeline_model = finetune(
                tokenizer, pipeline_model, lora_pipeline_path.as_posix()
            )
    return (tokenizer, embeding_model, pipeline_model)
