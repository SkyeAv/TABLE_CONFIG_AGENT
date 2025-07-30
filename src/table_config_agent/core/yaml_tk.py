__author__ = "Skye Lane Goetz"

from src.table_config_agent.core.utils import load_model, extension_from_url
from src.table_config_agent.models.template_cfg import Template
from ruamel.yaml.error import YAMLError
from typing import Any, Optional
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


def slim_to_template(
    slim_cfg: Any, config_curator_name: str, config_curator_organization: str
) -> Template:  # ensure slim_cfg is the result of .model_dump()

    pub = slim_cfg["pub"]
    url: str = str(slim_cfg["url"])  # so it parses as a string
    extension: str = extension_from_url(url)
    is_delim_file, sep_or_sheet = slim_cfg["ext_param"]
    start_at, end_at = slim_cfg["row_slice"]
    samp_is_col, samp_val = slim_cfg["samp"]
    p_val_is_col, p_val_val = slim_cfg["p_val"]
    fdr_is_col, fdr_val = slim_cfg["fdr"]
    rel_strength_is_col, rel_strength_val = slim_cfg["rel_strength"]
    method_is_col, method_val = slim_cfg["method"]
    subj_is_col, subj_val = slim_cfg["subj"]
    obj_is_col, obj_val = slim_cfg["obj"]
    pred = slim_cfg["pred"]
    taxon = slim_cfg["taxon"]
    boost_cls = slim_cfg["boost_cls"]
    boost_subj: list[str] = [category for col, categories in boost_cls if col for category in categories if category]
    boost_obj: list[str] = [category for col, categories in boost_cls if not col for category in categories if category]
    drop_cls = slim_cfg["drop_cls"]
    drop_subj: list[str] = [category for col, categories in drop_cls if col for category in categories if category]
    drop_obj: list[str] = [category for col, categories in drop_cls if not col for category in categories if category]

    template_cfg: dict[str, dict[str, Any]] = {
        "location": {
            "where_to_download_data_from": url,
            "download_hyperparameters": {
                "file_extension": extension,
                f'{"file_delimiter" if is_delim_file else "which_excel_sheet_to_use"}': sep_or_sheet,
                "start_at_line_number": start_at,
                "end_at_line_number": end_at,
            },
        },
        "provenance": {
            "publication": pub,
            "config_curator_name": config_curator_name,
            "config_curator_organization": config_curator_organization,
        },
        "attributes": {
            "sample_size": {
                "encoding_method": f'{"column_of_values" if samp_is_col else "value"}',
                "value_for_encoding": samp_val,
            },
            "p_value": {
                "encoding_method": f'{"column_of_values" if p_val_is_col else "value"}',
                "value_for_encoding": p_val_val,
            },
            "multiple_testing_correction_method": {
                "encoding_method": f'{"column_of_values" if fdr_is_col else "value"}',
                "value_for_encoding": fdr_val,
            },
            "relationship_strength": {
                "encoding_method": f'{"column_of_values" if rel_strength_is_col else "value"}',
                "value_for_encoding": rel_strength_val,
            },
            "assertion_method": {
                "encoding_method": f'{"column_of_values" if method_is_col else "value"}',
                "value_for_encoding": method_val,
            },
        },
        "triple": {
            "triple_subject": {
                "encoding_method": f'{"column_of_values" if subj_is_col else "value"}',
                "value_for_encoding": subj_val,
                "mapping_hyperparameters": {
                    "in_this_organism": taxon,
                    "classes_to_prioritize": boost_subj or None,
                    "classes_to_avoid": drop_subj or None,
                },
            },
            "triple_object": {
                "encoding_method": f'{"column_of_values" if obj_is_col else "value"}',
                "value_for_encoding": obj_val,
                "mapping_hyperparameters": {
                    "in_this_organism": taxon,
                    "classes_to_prioritize": boost_obj or None,
                    "classes_to_avoid": drop_obj or None,
                },
            },
            "triple_predicate": pred,
        },
    }

    return load_model(template_cfg, Template)  # type: ignore
