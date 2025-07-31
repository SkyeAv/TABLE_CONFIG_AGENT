from transformers import AutoTokenizer, AutoModel, BitsAndBytesConfig
import numpy as np
import random
import torch


def set_seed(seed: int) -> None:
    torch.manual_seed(seed)
    np.random.seed(seed)
    random.seed(seed)
    return None


def from_transformers(hf_model: str) -> tuple[AutoTokenizer, AutoModel]:
    tokenizer = AutoTokenizer.from_pretrained(hf_model)
    quantization = BitsAndBytesConfig(load_in_8bit=True)
    model = AutoModel.from_pretrained(
        hf_model,
        device_map="auto",
        quantization_config=quantization,
        torch_dtype="float16",
    )
    return (tokenizer, model)
