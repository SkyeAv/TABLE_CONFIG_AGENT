__author__ = "Skye Lane goetz"

from src.table_config_agent.core.yaml_tk import slim_to_template
from pydantic import HttpUrl
from typing import Any

example_01_slim: dict[str, Any] = {
    "pub": "PMID:39579765",
    "url": "https://www.cell.com/cms/10.1016/j.cell.2024.10.045/attachment/765b3106-d659-4412-a27b-b7e76d7895e9/mmc7.xlsx",
    "ext_param": (False, "Table S7"),
    "row_slice": (3, None),
    "samp": (False, 53026),
    "p_val": (True, "E"),
    "fdr": (False, "Bonferroni"),
    "rel_strength": (None, None),
    "method": (False, "Pathway score"),
    "subj": (True, "B"),
    "obj": (False, "multimorbidity"),
    "pred": "biolink:associated_with",
    "taxon": "NCBITaxon:9606",
    "boost_cls": [(True, ["biolink:Gene"])],
    "drop_cls": [(True, [None])],
}

expected_01_template: dict[str, Any] = {
    "location": {
        "where_to_download_data_from": HttpUrl(
            "https://www.cell.com/cms/10.1016/j.cell.2024.10.045/attachment/765b3106-d659-4412-a27b-b7e76d7895e9/mmc7.xlsx"
        ),
        "download_hyperparameters": {
            "file_extension": "xlsx",
            "which_excel_sheet_to_use": "Table S7",
            "start_at_line_number": 3,
            "end_at_line_number": None,
            "use_row_numbers": None,
        },
    },
    "provenance": {
        "publication": "PMID:39579765",
        "config_curator_name": "pytest",
        "config_curator_organization": "pytest",
    },
    "attributes": {
        "sample_size": {
            "encoding_method": "value",
            "value_for_encoding": 53026,
        },
        "p_value": {
            "encoding_method": "column_of_values",
            "value_for_encoding": "E",
        },
        "multiple_testing_correction_method": {
            "encoding_method": "value",
            "value_for_encoding": "Bonferroni",
        },
        "relationship_strength": {
            "encoding_method": "value",
            "value_for_encoding": None,
        },
        "assertion_method": {
            "encoding_method": "value",
            "value_for_encoding": "Pathway score",
        },
        "notes": None,
    },
    "triple": {
        "triple_subject": {
            "encoding_method": "column_of_values",
            "value_for_encoding": "B",
            "mapping_hyperparameters": {
                "in_this_organism": "NCBITaxon:9606",
                "classes_to_prioritize": ["biolink:Gene"],
                "classes_to_avoid": None,
            },
        },
        "triple_object": {
            "encoding_method": "value",
            "value_for_encoding": "multimorbidity",
            "mapping_hyperparameters": {
                "in_this_organism": "NCBITaxon:9606",
                "classes_to_prioritize": None,
                "classes_to_avoid": None,
            },
        },
        "triple_predicate": "biolink:associated_with",
    },
}

example_02_slim: dict[str, Any] = {
    "pub": "PMC:PMC11726441",
    "url": "https://static-content.springer.com/esm/art%3A10.1038%2Fs41564-024-01870-z/MediaObjects/41564_2024_1870_MOESM4_ESM.xlsx",
    "ext_param": (False, "Supplementary Table 13"),
    "row_slice": (2, None),
    "samp": (False, 21561),
    "p_val": (True, "G"),
    "fdr": (False, "Benjamini Hochberg"),
    "rel_strength": (True, "D"),
    "method": (False, "Spearman correlation"),
    "subj": (True, "A"),
    "obj": (True, "H"),
    "pred": "biolink:associated_with",
    "taxon": None,
    "boost_cls": [
        (True, ["biolink:OrganismTaxon"]),
        (False, ["biolink:OrganismTaxon"]),
    ],
    "drop_cls": [(True, ["biolink:Gene"])],
}

expected_02_template: dict[str, Any] = {
    "location": {
        "where_to_download_data_from": HttpUrl(
            "https://static-content.springer.com/esm/art%3A10.1038%2Fs41564-024-01870-z/MediaObjects/41564_2024_1870_MOESM4_ESM.xlsx"
        ),
        "download_hyperparameters": {
            "file_extension": "xlsx",
            "which_excel_sheet_to_use": "Supplementary Table 13",
            "start_at_line_number": 2,
            "end_at_line_number": None,
            "use_row_numbers": None,
        },
    },
    "provenance": {
        "publication": "PMC:PMC11726441",
        "config_curator_name": "pytest",
        "config_curator_organization": "pytest",
    },
    "attributes": {
        "sample_size": {
            "encoding_method": "value",
            "value_for_encoding": 21561,
        },
        "p_value": {
            "encoding_method": "column_of_values",
            "value_for_encoding": "G",
        },
        "multiple_testing_correction_method": {
            "encoding_method": "value",
            "value_for_encoding": "Benjamini Hochberg",
        },
        "relationship_strength": {
            "encoding_method": "column_of_values",
            "value_for_encoding": "D",
        },
        "assertion_method": {
            "encoding_method": "value",
            "value_for_encoding": "Spearman correlation",
        },
        "notes": None,
    },
    "triple": {
        "triple_subject": {
            "encoding_method": "column_of_values",
            "value_for_encoding": "A",
            "mapping_hyperparameters": {
                "in_this_organism": None,
                "classes_to_prioritize": ["biolink:OrganismTaxon"],
                "classes_to_avoid": ["biolink:Gene"],
            },
        },
        "triple_object": {
            "encoding_method": "column_of_values",
            "value_for_encoding": "H",
            "mapping_hyperparameters": {
                "in_this_organism": None,
                "classes_to_prioritize": ["biolink:OrganismTaxon"],
                "classes_to_avoid": None,
            },
        },
        "triple_predicate": "biolink:associated_with",
    },
}

example_03_slim: dict[str, Any] = {
    "pub": "PMC:PMC8400760",
    "url": "https://pmc.ncbi.nlm.nih.gov/articles/instance/8400760/bin/12866_2021_2282_MOESM2_ESM.xlsx",
    "ext_param": (False, "sig_corr_tar_6W"),
    "row_slice": (2, None),
    "samp": (False, 158),
    "p_val": (True, "D"),
    "fdr": (False, "Benjamini Hochberg"),
    "rel_strength": (True, "C"),
    "method": (False, "Spearman correlation"),
    "subj": (True, "A"),
    "obj": (True, "B"),
    "pred": "biolink:correlated_with",
    "taxon": None,
    "boost_cls": [(True, ["biolink:OrganismTaxon"])],
    "drop_cls": [(True, [None])],
}

expected_03_template: dict[str, Any] = {
    "location": {
        "where_to_download_data_from": HttpUrl(
            "https://pmc.ncbi.nlm.nih.gov/articles/instance/8400760/bin/12866_2021_2282_MOESM2_ESM.xlsx"
        ),
        "download_hyperparameters": {
            "file_extension": "xlsx",
            "which_excel_sheet_to_use": "sig_corr_tar_6W",
            "start_at_line_number": 2,
            "end_at_line_number": None,
            "use_row_numbers": None,
        },
    },
    "provenance": {
        "publication": "PMC:PMC8400760",
        "config_curator_name": "pytest",
        "config_curator_organization": "pytest",
    },
    "attributes": {
        "sample_size": {
            "encoding_method": "value",
            "value_for_encoding": 158,
        },
        "p_value": {
            "encoding_method": "column_of_values",
            "value_for_encoding": "D",
        },
        "multiple_testing_correction_method": {
            "encoding_method": "value",
            "value_for_encoding": "Benjamini Hochberg",
        },
        "relationship_strength": {
            "encoding_method": "column_of_values",
            "value_for_encoding": "C",
        },
        "assertion_method": {
            "encoding_method": "value",
            "value_for_encoding": "Spearman correlation",
        },
        "notes": None,
    },
    "triple": {
        "triple_subject": {
            "encoding_method": "column_of_values",
            "value_for_encoding": "A",
            "mapping_hyperparameters": {
                "in_this_organism": None,
                "classes_to_prioritize": ["biolink:OrganismTaxon"],
                "classes_to_avoid": None,
            },
        },
        "triple_object": {
            "encoding_method": "column_of_values",
            "value_for_encoding": "B",
            "mapping_hyperparameters": {
                "in_this_organism": None,
                "classes_to_prioritize": None,
                "classes_to_avoid": None,
            },
        },
        "triple_predicate": "biolink:correlated_with",
    },
}


def test_slim_to_template() -> None:
    assert (
        slim_to_template(example_01_slim, "pytest", "pytest").model_dump()
        == expected_01_template
    )
    assert (
        slim_to_template(example_02_slim, "pytest", "pytest").model_dump()
        == expected_02_template
    )
    assert (
        slim_to_template(example_03_slim, "pytest", "pytest").model_dump()
        == expected_03_template
    )
    return None
