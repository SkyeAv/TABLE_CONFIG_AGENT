from src.table_config_agent.chroma_db.template_examples import TEMPLATE_EXAMPLES
from src.table_config_agent.core.llms import from_transformers, set_seed
from langchain_chroma import Chroma
from transformers import AutoTokenizer, AutoModel
from langchain.embeddings.base import Embeddings
from langchain.schema import Document
from typing import Any, Self
from pathlib import Path
import torch


class HuggingFaceEmbeddings(Embeddings):
    def __init__(
        self: Self, tokenizer: AutoTokenizer, embedding_model: AutoModel
    ) -> None:
        super().__init__()
        self.embedding_model = embedding_model
        self.tokenizer = tokenizer
        return None

    def embed_documents(self: Self, texts: list[str]) -> list[list[float]]:
        return [self._embed_text(text) for text in texts]

    def embed_query(self, text: str) -> list[float]:
        return self._embed_text(text)

    def _embed_text(self, text: str) -> list[float]:
        inputs = self.tokenizer(  # type: ignore
            text, return_tensors="pt", truncation=True, padding=True, max_length=4096
        )
        inputs = {k: v.to(self.embedding_model.device) for k, v in inputs.items()}  # type: ignore
        with torch.no_grad():
            outputs = self.embedding_model(**inputs)  # type: ignore
        embedding = (
            outputs.last_hidden_state.mean(dim=1).squeeze().cpu().numpy().tolist()
        )
        return embedding  # type: ignore


def build_chroma_db(db_p: Path, cfg: dict[str, Any]) -> None:
    set_seed(cfg["seed"])  # set seed first
    tokenizer, embedding_model, _ = from_transformers(cfg["from_transformers"])
    template_docs: list[Document] = [
        Document(
            page_content=example["input"],  # just the Q:
            metadata={
                "formatted": f'Input: {example["input"]}\nOutput: {example["output"]}'
            },
        )
        for example in TEMPLATE_EXAMPLES
    ]
    _ = Chroma.from_documents(
        documents=template_docs,
        embedding=HuggingFaceEmbeddings(tokenizer, embedding_model),
        persist_directory=db_p.as_posix(),
        collection_name="template_examples",
    )
    return None
