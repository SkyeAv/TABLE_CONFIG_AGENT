__author__ = "Skye Lane Goetz"

from pydantic import BaseModel, Field, FilePath, field_validator
from huggingface_hub import HfApi, RepositoryNotFoundError

class ModelConfig(BaseModel):
    from_transformers: str = Field(...)
    using_chroma_db: FilePath = Field(...)
    seed: int = Field(...)

    @field_validator("from_transformers")
    def model_exists(cls, hypothetical_model: str) -> str:
        api: HfApi = HfApi()
        try:
            api.model_info(repo_id=hypothetical_model)
            return hypothetical_model
        except RepositoryNotFoundError:
            msg: str = f"CODE:1 | {hypothetical_model} must be a valid HuggingFace model"
            raise ValueError(msg)
        except Exception as e:
            msg = f"CODE:2 | error validating {hypothetical_model} | {str(e)}"
            raise RuntimeError(msg)