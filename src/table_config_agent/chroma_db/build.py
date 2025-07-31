from src.table_config_agent.chroma_db.template_examples import TEMPLATE_EXAMPLES
from src.table_config_agent.core.llms import from_transformers, set_seed
from langchain_community.vectorstores import Chroma
from transformers import AutoTokenizer, AutoModel
from langchain.embeddings.base import Embeddings
from langchain.schema import Document
from typing import Any, Self
from pathlib import Path
import torch


class HuggingFaceEmbeddings(Embeddings):  # type: ignore
    def __init__(self: Self, tokenizer: AutoTokenizer, model: AutoModel) -> None:
        super().__init__()
        self.model = model
        self.tokenizer = tokenizer
        return None

    def embed_documents(self: Self, texts: list[str]) -> list[list[float]]:
        return [self._embed_text(text) for text in texts]

    def embed_query(self, text: str) -> list[float]:
        return self._embed_text(text)

    def _embed_text(self, text: str) -> list[float]:
        inputs = self.tokenizer(
            text, return_tensors="pt", truncation=True, padding=True, max_length=4096
        )
        inputs = {k: v.to(self.model.device) for k, v in inputs.items()}
        with torch.no_grad():
            outputs = self.model(**inputs)
        embedding = (
            outputs.last_hidden_state.mean(dim=1).squeeze().cpu().numpy().tolist()
        )
        return embedding  # type: ignore


def build_chroma_db(db_p: Path, cfg: dict[str, Any]) -> None:
    set_seed(cfg["seed"])  # set seed first
    tokenizer, model = from_transformers(cfg["from_transformers"])
    template_docs: list[Document] = [
        Document(
            page_content=f"Q: {example.input}\nA: {example.output}",
            metadata={"input": example.input, "output": example.output},
        )
        for example in TEMPLATE_EXAMPLES
    ]
    db = Chroma.from_documents(
        documents=template_docs,
        embedding=HuggingFaceEmbeddings(tokenizer, model),
        persist_directory=db_p,
        collection_name="template_examples",
    )
    db.persist()
    return None
