from src.table_config_agent.chroma_db.template_examples import (
    TEMPLATE_EXAMPLES,
    Example,
)
from transformers.data.data_collator import DataCollatorForLanguageModeling
from transformers import AutoTokenizer, AutoModel, AutoModelForCausalLM
from src.table_config_agent.models.slim_cfg import SectionConfigSlim
from peft import get_peft_model, LoraConfig, TaskType, PeftModel
from langchain.output_parsers import PydanticOutputParser
from transformers.training_args import TrainingArguments
from langchain.prompts import PromptTemplate
from transformers.trainer import Trainer
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
    tokenizer: AutoTokenizer, batch: dict[str, Any], max_length: int
) -> dict[str, Any]:
    texts: list[str] = [
        p + tokenizer.pad_token + t for p, t in zip(batch["prompt"], batch["target"])  # type: ignore
    ]
    tokens = tokenizer(  # type: ignore
        texts, truncation=True, padding="max_length", max_length=max_length
    )

    labels = [seq.copy() for seq in tokens["input_ids"]]
    for i, pid in enumerate(
        tokenizer(  # type: ignore
            batch["prompt"],
            truncation=True,
            padding="max_length",
            max_length=max_length,
        )["input_ids"]
    ):
        prompt_len: int = sum(1 for token in pid if token != tokenizer.pad_token_id)  # type: ignore
        labels[i][:prompt_len] = [-100] * prompt_len  # ignore prompt tokens in loss

    tokens["labels"] = labels
    return tokens  # type: ignore


def finetuning_prompt() -> PromptTemplate:
    return PromptTemplate.from_template(
        """\
You are a Python dictionary generation assistant. Your task is to convert structured natural language
descriptions of tabular metadata into strictly valid Python dictionaries that match the provided schema exactly.

### Each input describes:
- the publication source (e.g., PMC ID)
- the tabular file location
- how specific columns map to fields (e.g., p-value, subject, object)
- optional enhancements such as boost classes or taxonomic context

### You MUST respond with:
- A single Python dictionary
- Fully valid Python (parsable by `ast.literal_eval`)
- Matching the schema structure and field types precisely
- Only include keys for fields the user explicitly mentioned; omit all others (Pydantic will apply defaults).

Output Schema (for reference only — do NOT include it in your output):
{pydantic_model}

### Output Rules:
- Respond ONLY with the dictionary — no explanations, no comments, no markdown, no formatting
- Use double quotes for all dictionary keys
- Use double quotes for all string values
- Use True / False (capitalized) for booleans
- Use None (or [None] for boost_cls or drop_cls) for missing or null values
- Use (True, "A") if the field maps to a column
- Use (False, "value") if the field is a fixed constant
- Use lists or tuple (as specified in examples) for any collection-type fields
- Do not use markdown, code blocks, or JSON
- Do not use single quotes — always use double quotes for keys and string values
- Never return type names like str, int, or list as values — always use real example values or None

### Now generate the dictionary for the following input:
{user_input}
"""
    )


def format_finetuning_prompt(user_input: str, pydantic_model: str) -> str:
    return finetuning_prompt().format(
        user_input=user_input,
        pydantic_model=pydantic_model,
    )


def train_dataset(tokenizer: AutoTokenizer, max_length: int = 512) -> Dataset:
    parser = PydanticOutputParser(pydantic_object=SectionConfigSlim)
    pydantic_model: str = parser.get_format_instructions()
    examples: list[Example] = TEMPLATE_EXAMPLES
    ds = Dataset.from_dict(
        {
            "prompt": [
                format_finetuning_prompt(ex["input"], pydantic_model) for ex in examples
            ],
            "target": [ex["output"] for ex in examples],
        }
    )
    ds = ds.map(
        (lambda x: tokenize_and_mask(tokenizer, x, max_length)),
        batched=True,
        remove_columns=["prompt", "target"],
    )
    ds.set_format("torch", columns=["input_ids", "attention_mask", "labels"])
    return ds


def finetune(
    tokenizer: AutoTokenizer,
    pipeline_model: AutoModelForCausalLM,
    posix_model_path: str,
) -> AutoModelForCausalLM:

    if tokenizer.pad_token_id is None:
        tokenizer.pad_token = tokenizer.eos_token or tokenizer.sep_token or ""
        tokenizer.pad_token_id = tokenizer.eos_token_id
    pipeline_model.config.pad_token_id = tokenizer.pad_token_id

    vocab_size: int = len(tokenizer)
    emb_size: int = pipeline_model.get_input_embeddings().weight.size(0)
    if vocab_size != emb_size:
        pipeline_model.resize_token_embeddings(vocab_size)

    lora = LoraConfig(
        task_type=TaskType.CAUSAL_LM,
        inference_mode=False,
        r=8,
        lora_alpha=16,
        lora_dropout=0.05,
    )
    pipeline_pfet = get_peft_model(pipeline_model, lora)  # type: ignore
    emb_size = pipeline_pfet.get_input_embeddings().weight.size(0)
    if vocab_size != emb_size:
        pipeline_pfet.resize_token_embeddings(vocab_size)
    pipeline_pfet.config.pad_token_id = tokenizer.pad_token_id
    args = TrainingArguments(
        output_dir=posix_model_path,
        overwrite_output_dir=True,
        num_train_epochs=5,
        learning_rate=5e-5,
        weight_decay=0.01,
        logging_strategy="no",
        label_names=["labels"],
        per_device_train_batch_size=1,
        gradient_accumulation_steps=4,
    )
    data_collator = DataCollatorForLanguageModeling(
        tokenizer=tokenizer,
        mlm=False,
    )
    trainer = Trainer(
        model=pipeline_pfet,
        args=args,
        train_dataset=train_dataset(tokenizer),
        data_collator=data_collator,
    )
    trainer.train()
    pipeline_pfet.save_pretrained(posix_model_path)
    return pipeline_pfet  # type: ignore


def from_transformers(
    hf_model: str, offload_folder: Path, lora_pipeline_path: Path
) -> tuple[AutoTokenizer, AutoModel, AutoModelForCausalLM]:
    with suppress_tqdm():

        try:
            tokenizer = AutoTokenizer.from_pretrained(hf_model, use_fast=True)  # type: ignore
            _ = tokenizer.tokenize("Hai")  # Force backend check
        except Exception:
            tokenizer = AutoTokenizer.from_pretrained(hf_model, use_fast=False)  # type: ignore
        if tokenizer.pad_token is None:
            tokenizer.pad_token = tokenizer.eos_token or tokenizer.sep_token or ""
        tokenizer.pad_token_id = tokenizer.pad_token_id or tokenizer.eos_token_id

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

        vocab_size: int = len(tokenizer)
        emb_size: int = pipeline_model.get_input_embeddings().weight.size(0)
        if vocab_size != emb_size:
            pipeline_model.resize_token_embeddings(vocab_size)
        pipeline_model.config.pad_token_id = tokenizer.pad_token_id

        adapter_config_path: Path = lora_pipeline_path / "adapter_config.json"
        if adapter_config_path.exists():
            pipeline_model = PeftModel.from_pretrained(
                pipeline_model,
                lora_pipeline_path.as_posix(),
                device_map="auto",
                torch_dtype="float16",
                offload_folder=offload_folder.as_posix(),
            )
            emb_size = pipeline_model.get_input_embeddings().weight.size(0)
            if vocab_size != emb_size:
                pipeline_model.resize_token_embeddings(vocab_size)
            pipeline_model.config.pad_token_id = tokenizer.pad_token_id
        else:
            pipeline_model = finetune(
                tokenizer, pipeline_model, lora_pipeline_path.as_posix()
            )
    return (tokenizer, embeding_model, pipeline_model)
