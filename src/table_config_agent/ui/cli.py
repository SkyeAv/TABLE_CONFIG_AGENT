from src.table_config_agent.core.utils import load_model, xz_backup
from src.table_config_agent.chroma_db.build import build_chroma_db
from src.table_config_agent.models.model_cfg import ModelConfig
from src.table_config_agent.core.yaml_tk import load_yaml
from pathlib import Path
from typing import Any
import typer

app = typer.Typer()


@app.command()  # type: ignore
def chroma_db(
    db_path: str = typer.Option(
        ...,
        "-p",
        "--db-path",
        help="path specifiying where you want to save and what you want to name the chroma_db build",
    ),
    model: str = typer.Option(
        ..., "-m", "--model-config", help="path to your ModelConfig (model.yaml)"
    ),
    backup: bool = typer.Option(
        False,
        "-b",
        "--backup-old-db",
        help="creates a timestamped xz compressed backup of the previous chroma_db build",
    ),
) -> None:
    """Builds the chroma_db for agent from examples in src.table_config_agent.chroma_db"""
    db_p: Path = Path(db_path).resolve()
    db_p.parent.mkdir(parents=True, exist_ok=True)
    model_p: Path = Path(model).resolve()
    if backup and db_p.is_file():
        xz_backup(db_p)
    model_yaml: Any = load_yaml(model_p)
    model_cfg: ModelConfig = load_model(model_yaml, ModelConfig)  # type: ignore
    build_chroma_db(db_p, model_cfg.model_dump())
    return None


def main() -> None:
    app()
    return None
