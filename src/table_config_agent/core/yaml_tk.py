__author__ = "Skye Lane Goetz"

from ruamel.yaml.error import YAMLError
from ruamel.yaml import YAML
from pathlib import Path

yaml = YAML()

def load_yaml(file_path: Path) -> Any:
    posix_file_path: str = file_path.as_posix()
    try:
        with file_path.open("r") as f:
            return yaml.load(f)
    except FileNotFoundError:
        msg: str = f"CODE:3 | {posix_file_path} not found"
        raise RuntimeError(msg)
    except PermissionError:
        msg = f"CODE:4 | Permission denied: {posix_file_path}"
        raise RuntimeError(msg)
    except YAMLError as e:
        err: str = str(e)
        msg = f"CODE:5 | YAML parsing error in {posix_file_path} | {err}"
        raise RuntimeError(msg)