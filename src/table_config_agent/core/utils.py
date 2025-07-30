__author__ = "Skye Lane Goetz"

from pydantic import ValidationError, BaseModel
from urllib.parse import urlparse
from typing import TypeVar, Any
from pathlib import PurePath
from textwrap import dedent


def collapse(x: str) -> str:
    return dedent(x).replace("\n", " ").strip()


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
