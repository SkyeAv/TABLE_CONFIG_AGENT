from src.table_config_agent.core.yaml_tk import slim_to_template, write_template
from src.table_config_agent.models.slim_cfg import SectionConfigSlim
from src.table_config_agent.chroma_db.build import build_chroma_db
from src.table_config_agent.core.utils import xz_backup, model_cfg
from src.table_config_agent.models.template_cfg import Template
from src.table_config_agent.core.chain import build_chain
from langchain_core.runnables import Runnable
from pathlib import Path
import typer

app = typer.Typer()


@app.command()
def chroma_build(
    db_path: str = typer.Option(
        "resources/chroma_db",
        "-d",
        "--db-path",
        help="path specifiying the directory where you want to save the chroma_db build",
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
    build_chroma_db(db_p, model_cfg(model_p))
    return None


@app.command()
def invoke_agent(
    user_input: str = typer.Option(
        ...,
        "-i",
        "--user-input",
        help="freetext input that the TableConfigAgent attempts to generate a TableConfig from",
    ),
    user_name: str = typer.Option(
        ...,
        "-n",
        "--user-name",
        help="your name, its required to build a valid TableConfig",
    ),
    user_organization: str = typer.Option(
        ...,
        "-o",
        "--user-organization",
        help="the organization you represent, its required to build a valid TableConfig",
    ),
    output_path: str = typer.Option(
        "resources/config/table/table_config.yaml",
        "-p",
        "--output-path",
        help="path specifiying where you want to save your TableConfig.yaml",
    ),
    model: str = typer.Option(
        ..., "-m", "--model-config", help="path to your ModelConfig (model.yaml)"
    ),
) -> None:
    model_p: Path = Path(model).resolve()
    output_p: Path = Path(output_path).resolve()
    output_p.parent.mkdir(parents=True, exist_ok=True)
    chain: Runnable = build_chain(model_cfg(model_p))  # type: ignore
    output: SectionConfigSlim = chain.invoke(user_input)
    template: Template = slim_to_template(output, user_name, user_organization)
    write_template(template.model_dump(), output_p)
    return None


def main() -> None:
    app()
    return None
