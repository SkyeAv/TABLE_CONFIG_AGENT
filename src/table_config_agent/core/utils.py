from src.table_config_agent.models.model_cfg import ModelConfig
from pydantic import ValidationError, BaseModel
from pathlib import Path, PurePath
from urllib.parse import urlparse
from typing import TypeVar, Any
from datetime import datetime
from textwrap import dedent
import shutil
import lzma
import re

MODEL_CACHE: Path = Path("CACHE/MODELS/").resolve()
MODEL_CACHE.mkdir(parents=True, exist_ok=True)


def collapse(x: str) -> str:
    x = dedent(x).strip()
    return re.sub(r"\s+", " ", x)


PydanticModel = TypeVar("PydanticModel", bound=BaseModel)


def load_model(python_object: Any, pydantic_model: PydanticModel) -> PydanticModel:
    try:
        return pydantic_model.model_validate(python_object)
    except ValidationError as e:
        msg: str = f"CODE:6 | Failed to parse to {pydantic_model.__name__} | {str(e)}"  # type: ignore
        raise RuntimeError(msg)


def extension_from_url(url: str) -> str:  # xlsx is default b/c its the most common
    urlpath = urlparse(url).path
    pure_urlpath: PurePath = PurePath(urlpath)
    return "".join(pure_urlpath.suffixes)[1:] or "xlsx"


def xz_backup(db_p: Path, fmt: str = r"%Y%m%d") -> None:
    timestamp: str = datetime.now().strftime(fmt)
    xz_p = db_p.with_name(db_p.stem + timestamp + db_p.suffix + ".xz")
    with db_p.open("rb") as f_in, lzma.open(xz_p, "wb") as f_out:
        shutil.copyfileobj(f_in, f_out)
    return None


def model_cfg(model_p: Path) -> dict[str, Any]:
    from src.table_config_agent.core.yaml_tk import (
        load_yaml,
    )  # circular import prevention... yay!

    model_yaml: Any = load_yaml(model_p)
    return load_model(model_yaml, ModelConfig).model_dump()  # type: ignore
