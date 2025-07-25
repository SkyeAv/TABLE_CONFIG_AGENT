__author__ = "Skye Lane Goetz"

from pydantic import BaseModel, HttpUrl, Field
from typing import Optional


# the only reason I'm making a slim config is so I don't explode the models context window
class SectionConfigSlim(BaseModel):

    pub: str = Field(..., description="pub:str-pubCurie")
    url: HttpUrl = Field(..., description="url:URL-download")
    ext_param: tuple[bool, str] = Field(
        default=(False, "Sheet1"),
        description="ext_paramFlg:bool-isDelim|ext_paramVal:str-sepOrSheet",
    )
    row_slice: tuple[Optional[int], Optional[int]] = Field(
        default=(None, None), description="rowStart:idx?-start|rowEnd:idx?-end"
    )

    samp: tuple[Optional[bool], Optional[str]] = Field(
        default=(None, None), description="sampFlg:bool?-isCol|sampVal:str?-val"
    )
    p_val: tuple[Optional[bool], Optional[str]] = Field(
        default=(None, None), description="p_valFlg:bool?-isCol|p_valVal:str?-val"
    )
    fdr: tuple[Optional[bool], Optional[str]] = Field(
        default=(None, None), description="fdrFlg:bool?-isCol|fdrVal:str?-val"
    )
    rel_strength: tuple[Optional[bool], Optional[str]] = Field(
        default=(None, None),
        description="rel_strengthFlg:bool?-isCol|rel_strengthVal:str?-val",
    )
    method: tuple[Optional[bool], Optional[str]] = Field(
        default=(None, None), description="methodFlg:bool?-isCol|methodVal:str?-val"
    )

    subj: tuple[bool, str] = Field(
        ..., description="subjFlg:bool-isCol|subjVal:str-val"
    )
    obj: tuple[bool, str] = Field(..., description="objFlg:bool-isCol|objVal:str-val")
    pred: str = Field(..., description="predVal:str-biolinkPred")

    taxon: Optional[str] = Field(default=None, description="taxon:str?-ncbiTaxId")
    boost_cls: list[tuple[bool, list[Optional[str]]]] = Field(
        default=[(True, [None])],
        description="boost_cls:list-(boost_clsFlg:bool-isSubj|boost_clsVal:list?-prioritize)",
    )
    drop_cls: list[tuple[bool, list[Optional[str]]]] = Field(
        default=[(True, [None])],
        description="drop_cls:list-(drop_clsFlg:bool-isSubj|drop_clsVal:list?-avoid)",
    )
