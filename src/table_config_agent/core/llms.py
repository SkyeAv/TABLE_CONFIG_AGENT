from transformers import AutoTokenizer, AutoModel, AutoModelForCausalLM
from contextlib import contextmanager
from typing import ContextManager
from pathlib import Path
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


def from_transformers(
    hf_model: str, offload_folder: Path
) -> tuple[AutoTokenizer, AutoModel, AutoModelForCausalLM]:
    try:
        tokenizer = AutoTokenizer.from_pretrained(hf_model, use_fast=True)  # type: ignore
        _ = tokenizer.tokenize("Hai")  # Force backend check
    except Exception:
        tokenizer = AutoTokenizer.from_pretrained(hf_model, use_fast=False)  # type: ignore
    with suppress_tqdm():
        embeding_model = AutoModel.from_pretrained(
            hf_model, device_map={"": "cpu"}, torch_dtype="float16"
        ).eval()
        pipeline_model = AutoModelForCausalLM.from_pretrained(
            hf_model,
            device_map="auto",
            torch_dtype="float16",
            offload_folder=offload_folder.as_posix(),
            offload_state_dict=True,
            low_cpu_mem_usage=True,
        ).eval()
    return (tokenizer, embeding_model, pipeline_model)
