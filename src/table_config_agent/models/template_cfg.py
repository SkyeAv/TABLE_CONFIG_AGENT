from typing import Optional, Annotated, TypeAlias, Literal, Union
from pydantic import BaseModel, HttpUrl, Field


class ExcelHyperparameters(BaseModel):
    file_extension: Literal["xlsx", "xls"] = Field(...)
    which_excel_sheet_to_use: Optional[str] = Field(default=None)
    start_at_line_number: Optional[int] = Field(default=None)
    end_at_line_number: Optional[int] = Field(default=None)
    use_row_numbers: Optional[list[int]] = Field(default=None)


class CsvHyperparameters(BaseModel):
    file_extension: Literal["csv", "tsv", "txt"] = Field(...)
    file_delimiter: Optional[str] = Field(default=None)
    start_at_line_number: Optional[int] = Field(default=None)
    end_at_line_number: Optional[int] = Field(default=None)
    use_row_numbers: Optional[list[int]] = Field(default=None)


DownloadHyperparameters: TypeAlias = Annotated[
    Union[ExcelHyperparameters, CsvHyperparameters],
    Field(discriminator="file_extension"),
]


class Location(BaseModel):
    where_to_download_data_from: Optional[HttpUrl] = Field(default=None)
    download_hyperparameters: Optional[DownloadHyperparameters] = Field(default=None)


class Provenance(BaseModel):
    publication: Optional[str] = Field(default=None)
    config_curator_name: Optional[str] = Field(default=None)
    config_curator_organization: Optional[str] = Field(default=None)


class Attribute(BaseModel):
    encoding_method: Optional[Literal["value", "column_of_values"]] = Field(
        default=None
    )
    value_for_encoding: Optional[Union[float, str, int]] = Field(default=None)


class Attributes(BaseModel):
    sample_size: Attribute = Field(default_factory=Attribute)
    p_value: Attribute = Field(default_factory=Attribute)
    multiple_testing_correction_method: Attribute = Field(default_factory=Attribute)
    relationship_strength: Attribute = Field(default_factory=Attribute)
    assertion_method: Attribute = Field(default_factory=Attribute)
    notes: Optional[str] = Field(default=None)


class MappingHyperparameters(BaseModel):
    in_this_organism: Optional[str] = Field(default=None)
    classes_to_prioritize: Optional[list[str]] = Field(default=None)
    classes_to_avoid: Optional[list[str]] = Field(default=None)


class GraphVertex(BaseModel):
    encoding_method: Optional[Literal["value", "column_of_values"]] = Field(
        default=None
    )
    value_for_encoding: Optional[str] = Field(default=None)
    mapping_hyperparameters: MappingHyperparameters = Field(
        default_factory=MappingHyperparameters
    )


class Triple(BaseModel):
    triple_subject: GraphVertex = Field(default_factory=GraphVertex)
    triple_object: GraphVertex = Field(default_factory=GraphVertex)
    triple_predicate: Optional[str] = Field(default=None)


class Template(BaseModel):
    location: Optional[Location] = Field(default=None)
    provenance: Optional[Provenance] = Field(default=None)
    attributes: Optional[Attributes] = Field(default=None)
    triple: Optional[Triple] = Field(default=None)
