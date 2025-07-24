__author__ = "Skye Lane Goetz"

from langchain.schema import Example
from textwrap import dedent

def collapse(x: str) -> str:
    return dedent(x).replace("\n", " ").strip()

EXAMPLES: list[Example] = [

    Example(
        input=collapse("""
            article is PMC:PMC9691620
            use Table S3 from it
            from https://pmc.ncbi.nlm.nih.gov/articles/instance/9691620/bin/NIHMS1845232-supplement-1845232_Sup_Tab_1-5.xlsx
            these are associations
            and the subject is in column B and prioritize biolink:OrganismTaxon
            and the object is in column O
            while the p values are in F and they used a Bonferroni correction
            the sample size is 3064
            relationship strength is in column E and its a Two-sided Wald test
        """),
        output=collapse("""{
            "pub": "PMC:PMC9691620",
            "url": "https://pmc.ncbi.nlm.nih.gov/articles/instance/9691620/bin/NIHMS1845232-supplement-1845232_Sup_Tab_1-5.xlsx,"
            "ext_param": (False, "Table S3"),

            "samp": (False, 3064),
            "p_val": (True, "F"),
            "fdr": (False, "Bonferroni"),
            "rel_strength": (True, "E"),
            "method": (False, "Two-sided Wald test"),

            "subj": (True, "O"),
            "obj": (True, "B"),
            "pred": "biolink:associated_with",

            "taxon": str,
            "boost_cls": [
                (False, ["biolink:OrganismTaxon"]),
            ],
        }"""),
    ),

    Example(
        input=collapse("""
            PMC9691620
            https://pmc.ncbi.nlm.nih.gov/articles/instance/9691620/bin/NIHMS1845232-supplement-1845232_Sup_Tab_1-5.xlsx
            Table S3
            biolink:associated_with
            subject=B
            object=O (biolink:OrganismTaxon)
            Bonferroni
            n = 3064
            p = F
            strength = E
            Two-sided Wald test
        """),
        output=collapse("""{
            "pub": "PMC:PMC9691620",
            "url": "https://pmc.ncbi.nlm.nih.gov/articles/instance/9691620/bin/NIHMS1845232-supplement-1845232_Sup_Tab_1-5.xlsx,"
            "ext_param": (False, "Table S3"),

            "samp": (False, 3064),
            "p_val": (True, "F"),
            "fdr": (False, "Bonferroni"),
            "rel_strength": (True, "E"),
            "method": (False, "Two-sided Wald test"),

            "subj": (True, "O"),
            "obj": (True, "B"),
            "pred": "biolink:associated_with",

            "taxon": str,
            "boost_cls": [
                (False, ["biolink:OrganismTaxon"]),
            ],
        }"""),
    ),

    Example(
        input=collapse("""
            From https://pmc.ncbi.nlm.nih.gov/articles/instance/9691620/bin/NIHMS1845232-supplement-1845232_Sup_Tab_1-5.xlsx, Table S3
            the subject is in col B,
            the predicate is biolink:associated_with,
            and the object is in column O.
            The object is a taxon.
            n = 3064
            p = col F
            fdr = Bonferroni
            relationship_strength = E (Two-sided Wald test)
            The artcle from pubmed central is PMC9691620
        """),
        output=collapse("""{
            "pub": "PMC:PMC9691620",
            "url": "https://pmc.ncbi.nlm.nih.gov/articles/instance/9691620/bin/NIHMS1845232-supplement-1845232_Sup_Tab_1-5.xlsx,"
            "ext_param": (False, "Table S3"),

            "samp": (False, 3064),
            "p_val": (True, "F"),
            "fdr": (False, "Bonferroni"),
            "rel_strength": (True, "E"),
            "method": (False, "Two-sided Wald test"),

            "subj": (True, "O"),
            "obj": (True, "B"),
            "pred": "biolink:associated_with",

            "taxon": str,
            "boost_cls": [
                (False, ["biolink:OrganismTaxon"]),
            ],
        }"""),
    ),

    Example(
        input=collapse("""
            Fackle
        """),
        output=collapse("""{
            "pub": "PMC:PMC11726441",
            "url": "https://static-content.springer.com/esm/art%3A10.1038%2Fs41564-024-01870-z/MediaObjects/41564_2024_1870_MOESM4_ESM.xlsx,"
            "ext_param": (False, "Supplementary Table 13"),
            "row_slice": (2, None),

            "samp": (False, 21561),
            "p_val": (True, "G"),
            "fdr": (False, "Benjamini Hochberg"),
            "method": (False, "Spearman correlation"),

            "subj": (True, "A"),
            "obj": (True, "H"),
            "pred": "biolink:associated_with",

            "drop_cls": [
                (True, ["biolink:OrganismTaxon"]),
                (False, ["biolink:OrganismTaxon"]),
            ],
        }"""),
    ),

    Example(
        input=collapse("""
            Fackle
        """),
        output=collapse("""{
            "pub": "PMC:PMC11726441",
            "url": "https://static-content.springer.com/esm/art%3A10.1038%2Fs41564-024-01870-z/MediaObjects/41564_2024_1870_MOESM4_ESM.xlsx,"
            "ext_param": (False, "Supplementary Table 13"),
            "row_slice": (2, None),

            "samp": (False, 21561),
            "p_val": (True, "G"),
            "fdr": (False, "Benjamini Hochberg"),
            "method": (False, "Spearman correlation"),

            "subj": (True, "A"),
            "obj": (True, "H"),
            "pred": "biolink:associated_with",

            "drop_cls": [
                (True, ["biolink:OrganismTaxon"]),
                (False, ["biolink:OrganismTaxon"]),
            ],
        }"""),
    ),

    Example(
        input=collapse("""
            Fackle
        """),
        output=collapse("""{
            "pub": "PMC:PMC11726441",
            "url": "https://static-content.springer.com/esm/art%3A10.1038%2Fs41564-024-01870-z/MediaObjects/41564_2024_1870_MOESM4_ESM.xlsx,"
            "ext_param": (False, "Supplementary Table 13"),
            "row_slice": (2, None),

            "samp": (False, 21561),
            "p_val": (True, "G"),
            "fdr": (False, "Benjamini Hochberg"),
            "method": (False, "Spearman correlation"),

            "subj": (True, "A"),
            "obj": (True, "H"),
            "pred": "biolink:associated_with",

            "drop_cls": [
                (True, ["biolink:OrganismTaxon"]),
                (False, ["biolink:OrganismTaxon"]),
            ],
        }"""),
    ),

    Example(
        input=collapse("""
            Fuess
        """),
        output=collapse("""{
            "pub": "PMC:PMC8262870",
            "url": "https://pmc.ncbi.nlm.nih.gov/articles/instance/8262870/bin/mbio.00145-21-sd002.xlsx",
            "ext_param": (False, "Geodermatophilaceae"),
            "row_slice": (2, None),

            "samp": (False, 1929),
            "rel_strength": (True, "D"),
            "method": (False, "Signed network using bicor analyses"),

            "subj": (False, "Geodermatophilaceae"),
            "obj": (True, "C"),
            "pred": "biolink:correlated_with",

            "taxon": "NCBITaxon:69293,"
            "boost_cls": [
                (True, ["biolink:OrganismTaxon"]),
            ],
        }"""),
    ),

    Example(
        input=collapse("""
            Fuess
        """),
        output=collapse("""{
            "pub": "PMC:PMC8262870",
            "url": "https://pmc.ncbi.nlm.nih.gov/articles/instance/8262870/bin/mbio.00145-21-sd002.xlsx",
            "ext_param": (False, "Geodermatophilaceae"),
            "row_slice": (2, None),

            "samp": (False, 1929),
            "rel_strength": (True, "D"),
            "method": (False, "Signed network using bicor analyses"),

            "subj": (False, "Geodermatophilaceae"),
            "obj": (True, "C"),
            "pred": "biolink:correlated_with",

            "taxon": "NCBITaxon:69293,"
            "boost_cls": [
                (True, ["biolink:OrganismTaxon"]),
            ],
        }"""),
    ),

    Example(
        input=collapse("""
            Fuess
        """),
        output=collapse("""{
            "pub": "PMC:PMC8262870",
            "url": "https://pmc.ncbi.nlm.nih.gov/articles/instance/8262870/bin/mbio.00145-21-sd002.xlsx",
            "ext_param": (False, "Geodermatophilaceae"),
            "row_slice": (2, None),

            "samp": (False, 1929),
            "rel_strength": (True, "D"),
            "method": (False, "Signed network using bicor analyses"),

            "subj": (False, "Geodermatophilaceae"),
            "obj": (True, "C"),
            "pred": "biolink:correlated_with",

            "taxon": "NCBITaxon:69293,"
            "boost_cls": [
                (True, ["biolink:OrganismTaxon"]),
            ],
        }"""),
    ),

    Example(
        input=collapse("""
            Lui
        """),
        output=collapse("""{
            "pub": "PMC:PMC10052271",
            "url": "https://static-content.springer.com/esm/art%3A10.1038%2Fs41598-023-31115-8/MediaObjects/41598_2023_31115_MOESM7_ESM.xlsx",
            "ext_param": (False, "Supplementary Table 6"),
            "row_slice": (2, None),

            "samp": (True, "L"),
            "p_val": (True, "K"),
            "rel_strength": (True, "I"),
            "method": (False, "Generalised summary-data-based Mendelian randomization"),

            "subj": (True, "H"),
            "obj": (False, "longevity"),
            "pred": "biolink:affects",

            "boost_cls": [
                (False, ["biolink:PhenotypicFeature", "biolink:ClinicalFinding"]),
                (True, ["biolink:OrganismTaxon"]),
            ],
            "drop_cls": [
                (False, ["biolink:Gene"]),
            ],
        }"""),
    ),


    Example(
        input=collapse("""
            Lui
        """),
        output=collapse("""{
            "pub": "PMC:PMC10052271",
            "url": "https://static-content.springer.com/esm/art%3A10.1038%2Fs41598-023-31115-8/MediaObjects/41598_2023_31115_MOESM7_ESM.xlsx",
            "ext_param": (False, "Supplementary Table 6"),
            "row_slice": (2, None),

            "samp": (True, "L"),
            "p_val": (True, "K"),
            "rel_strength": (True, "I"),
            "method": (False, "Generalised summary-data-based Mendelian randomization"),

            "subj": (True, "H"),
            "obj": (False, "longevity"),
            "pred": "biolink:affects",

            "boost_cls": [
                (False, ["biolink:PhenotypicFeature", "biolink:ClinicalFinding"]),
                (True, ["biolink:OrganismTaxon"]),
            ],
            "drop_cls": [
                (False, ["biolink:Gene"]),
            ],
        }"""),
    ),

    Example(
        input=collapse("""
            Lui
        """),
        output=collapse("""{
            "pub": "PMC:PMC10052271",
            "url": "https://static-content.springer.com/esm/art%3A10.1038%2Fs41598-023-31115-8/MediaObjects/41598_2023_31115_MOESM7_ESM.xlsx",
            "ext_param": (False, "Supplementary Table 6"),
            "row_slice": (2, None),

            "samp": (True, "L"),
            "p_val": (True, "K"),
            "rel_strength": (True, "I"),
            "method": (False, "Generalised summary-data-based Mendelian randomization"),

            "subj": (True, "H"),
            "obj": (False, "longevity"),
            "pred": "biolink:affects",

            "boost_cls": [
                (False, ["biolink:PhenotypicFeature", "biolink:ClinicalFinding"]),
                (True, ["biolink:OrganismTaxon"]),
            ],
            "drop_cls": [
                (False, ["biolink:Gene"]),
            ],
        }"""),
    ),

    Example(
        input=collapse("""
            Pu
        """),
        output=collapse("""{
            "pub": "PMID:39054372",
            "url": "https://static-content.springer.com/esm/art%3A10.1038%2Fs43587-024-00678-0/MediaObjects/43587_2024_678_MOESM12_ESM.csv",
            "ext_param": (True, ","),

            "samp": (False, 1448),
            "p_val": (True, "D"),
            "fdr": (False, "Benjamini Hochberg"),
            "rel_strength": (True, "C"),
            "method": (False, "Linear regression"),

            "subj": (True, "A"),
            "obj": (True, "B"),
            "pred": "biolink:associated_with",

            "boost_cls": [
                (True, ["biolink:OrganismTaxon"]),
        }"""),
    ),

    Example(
        input=collapse("""
            Pu
        """),
        output=collapse("""{
            "pub": "PMID:39054372",
            "url": "https://static-content.springer.com/esm/art%3A10.1038%2Fs43587-024-00678-0/MediaObjects/43587_2024_678_MOESM12_ESM.csv",
            "ext_param": (True, ","),

            "samp": (False, 1448),
            "p_val": (True, "D"),
            "fdr": (False, "Benjamini Hochberg"),
            "rel_strength": (True, "C"),
            "method": (False, "Linear regression"),

            "subj": (True, "A"),
            "obj": (True, "B"),
            "pred": "biolink:associated_with",

            "boost_cls": [
                (True, ["biolink:OrganismTaxon"]),
        }"""),
    ),

    Example(
        input=collapse("""
            Pu
        """),
        output=collapse("""{
            "pub": "PMID:39054372",
            "url": "https://static-content.springer.com/esm/art%3A10.1038%2Fs43587-024-00678-0/MediaObjects/43587_2024_678_MOESM12_ESM.csv",
            "ext_param": (True, ","),

            "samp": (False, 1448),
            "p_val": (True, "D"),
            "fdr": (False, "Benjamini Hochberg"),
            "rel_strength": (True, "C"),
            "method": (False, "Linear regression"),

            "subj": (True, "A"),
            "obj": (True, "B"),
            "pred": "biolink:associated_with",

            "boost_cls": [
                (True, ["biolink:OrganismTaxon"]),
        }"""),
    ),

    Example(
        input=collapse("""
            Qin
        """),
        output=collapse("""{
            "pub": "PMC:PMC11401200",
            "url": "https://pmc.ncbi.nlm.nih.gov/articles/instance/11401200/bin/mmc3.xlsx",
            "ext_param": (False, "Sheet1"),
            "row_slice": (None, 200000),

            "samp": (False, 969),
            "rel_strength": (True, "C"),
            "method": (False, "LASSO Regression"),

            "subj": (True, "E"),
            "obj": (True, "B"),
            "pred": "biolink:associated_with_resistance_to",

            "taxon": "NCBITaxon:9606",
            "boost_cls": [
                (True, ["biolink:Gene"]),
                (False, ["biolink:Gene"]),
            ],
        }"""),
    ),

    Example(
        input=collapse("""
            Qin
        """),
        output=collapse("""{
            "pub": "PMC:PMC11401200",
            "url": "https://pmc.ncbi.nlm.nih.gov/articles/instance/11401200/bin/mmc3.xlsx",
            "ext_param": (False, "Sheet1"),
            "row_slice": (None, 200000),

            "samp": (False, 969),
            "rel_strength": (True, "C"),
            "method": (False, "LASSO Regression"),

            "subj": (True, "E"),
            "obj": (True, "B"),
            "pred": "biolink:associated_with_resistance_to",

            "taxon": "NCBITaxon:9606",
            "boost_cls": [
                (True, ["biolink:Gene"]),
                (False, ["biolink:Gene"]),
            ],
        }"""),
    ),

    Example(
        input=collapse("""
            Qin
        """),
        output=collapse("""{
            "pub": "PMC:PMC11401200",
            "url": "https://pmc.ncbi.nlm.nih.gov/articles/instance/11401200/bin/mmc3.xlsx",
            "ext_param": (False, "Sheet1"),
            "row_slice": (None, 200000),

            "samp": (False, 969),
            "rel_strength": (True, "C"),
            "method": (False, "LASSO Regression"),

            "subj": (True, "E"),
            "obj": (True, "B"),
            "pred": "biolink:associated_with_resistance_to",

            "taxon": "NCBITaxon:9606",
            "boost_cls": [
                (True, ["biolink:Gene"]),
                (False, ["biolink:Gene"]),
            ],
        }"""),
    ),

    Example(
        input=collapse("""
            Romero
        """),
        output=collapse("""{
            "pub": "PMC:PMC10434204",
            "url": "https://pmc.ncbi.nlm.nih.gov/articles/instance/10434204/bin/spectrum.03429-22-s0001.xlsx",
            "ext_param": (False, "SupplementalTable_3"),
            "row_slice": (5, None),

            "samp": (False, 474),
            "p_val": (True, "H"),
            "fdr": (False, "FDR of 10 percent"),
            "rel_strength": (True, "E"),
            "method": (False, "LME model"),

            "subj": (True, "B"),
            "obj": (True, "D"),
            "pred": "biolink:associated_with",

            "boost_cls": [
                (True, ["biolink:OrganismTaxon"]),
                (False, ["biolink:OrganismTaxon"]),
            ],
        }"""),
    ),

    Example(
        input=collapse("""
            Romero
        """),
        output=collapse("""{
            "pub": "PMC:PMC10434204",
            "url": "https://pmc.ncbi.nlm.nih.gov/articles/instance/10434204/bin/spectrum.03429-22-s0001.xlsx",
            "ext_param": (False, "SupplementalTable_3"),
            "row_slice": (5, None),

            "samp": (False, 474),
            "p_val": (True, "H"),
            "fdr": (False, "FDR of 10 percent"),
            "rel_strength": (True, "E"),
            "method": (False, "LME model"),

            "subj": (True, "B"),
            "obj": (True, "D"),
            "pred": "biolink:associated_with",

            "boost_cls": [
                (True, ["biolink:OrganismTaxon"]),
                (False, ["biolink:OrganismTaxon"]),
            ],
        }"""),
    ),


    Example(
        input=collapse("""
            Romero
        """),
        output=collapse("""{
            "pub": "PMC:PMC10434204",
            "url": "https://pmc.ncbi.nlm.nih.gov/articles/instance/10434204/bin/spectrum.03429-22-s0001.xlsx",
            "ext_param": (False, "SupplementalTable_3"),
            "row_slice": (5, None),

            "samp": (False, 474),
            "p_val": (True, "H"),
            "fdr": (False, "FDR of 10 percent"),
            "rel_strength": (True, "E"),
            "method": (False, "LME model"),

            "subj": (True, "B"),
            "obj": (True, "D"),
            "pred": "biolink:associated_with",

            "boost_cls": [
                (True, ["biolink:OrganismTaxon"]),
                (False, ["biolink:OrganismTaxon"]),
            ],
        }"""),
    ),

    Example(
        input=collapse("""
            Wang
        """),
        output=collapse("""{
            "pub": "PMC:PMC6555748",
            "url": "https://pmc.ncbi.nlm.nih.gov/articles/instance/6555748/bin/12931_2019_1085_MOESM5_ESM.xlsx",
            "ext_param": (False, "A. Th1 and Th2 pathway"),
            "row_slice": (3, None),

            "samp": (False, "59"),
            "p_val": (True, "C"),
            "fdr": (False, "Benjamini Hochberg"),
            "rel_strength": (True, "D"),
            "method": (False, "Spearman correlation"),

            "subj": (True, "A"),
            "obj": (False, "Haemophilus"),
            "pred": "biolink:associated_with",

            "taxon": "NCBITaxon:9606",
            "boost_cls": [
                (True, ["biolink:Gene"]),
                (False, ["biolink:OrganismTaxon"]),
            ],
            "drop_cls": [
                (True, ["biolink:Protein"]),
            ],
        }"""),
    ),

    Example(
        input=collapse("""
            Wang
        """),
        output=collapse("""{
            "pub": "PMC:PMC6555748",
            "url": "https://pmc.ncbi.nlm.nih.gov/articles/instance/6555748/bin/12931_2019_1085_MOESM5_ESM.xlsx",
            "ext_param": (False, "A. Th1 and Th2 pathway"),
            "row_slice": (3, None),

            "samp": (False, "59"),
            "p_val": (True, "C"),
            "fdr": (False, "Benjamini Hochberg"),
            "rel_strength": (True, "D"),
            "method": (False, "Spearman correlation"),

            "subj": (True, "A"),
            "obj": (False, "Haemophilus"),
            "pred": "biolink:associated_with",

            "taxon": "NCBITaxon:9606",
            "boost_cls": [
                (True, ["biolink:Gene"]),
                (False, ["biolink:OrganismTaxon"]),
            ],
            "drop_cls": [
                (True, ["biolink:Protein"]),
            ],
        }"""),
    ),

    Example(
        input=collapse("""
            Wang
        """),
        output=collapse("""{
            "pub": "PMC:PMC6555748",
            "url": "https://pmc.ncbi.nlm.nih.gov/articles/instance/6555748/bin/12931_2019_1085_MOESM5_ESM.xlsx",
            "ext_param": (False, "A. Th1 and Th2 pathway"),
            "row_slice": (3, None),

            "samp": (False, "59"),
            "p_val": (True, "C"),
            "fdr": (False, "Benjamini Hochberg"),
            "rel_strength": (True, "D"),
            "method": (False, "Spearman correlation"),

            "subj": (True, "A"),
            "obj": (False, "Haemophilus"),
            "pred": "biolink:associated_with",

            "taxon": "NCBITaxon:9606",
            "boost_cls": [
                (True, ["biolink:Gene"]),
                (False, ["biolink:OrganismTaxon"]),
            ],
            "drop_cls": [
                (True, ["biolink:Protein"]),
            ],
        }"""),
    ),

    Example(
        input=collapse("""
            Wu
        """),
        output=collapse("""{
            "pub": "PMC:PMC11166937",
            "url": "https://pmc.ncbi.nlm.nih.gov/articles/instance/11166937/bin/41467_2023_42013_MOESM4_ESM.csv",
            "ext_param": (True, ","),

            "samp": (False, 27),
            "p_val": (True, "F"),
            "fdr": (False, "Benjamini Hochberg"),
            "rel_strength": (True, "C"),
            "method": (False, "Log2 Fold Change From Fishers Exact Test"),

            "subj": (False, "microgravity"),
            "obj": (True, "A"),
            "pred": "biolink:affects",

            "taxon": "NCBITaxon:9606",
            "boost_cls": [
                (False, ["biolink:Gene", "biolink:OrganismTaxon"]),
            ],
        }"""),
    ),

    Example(
        input=collapse("""
            Wu
        """),
        output=collapse("""{
            "pub": "PMC:PMC11166937",
            "url": "https://pmc.ncbi.nlm.nih.gov/articles/instance/11166937/bin/41467_2023_42013_MOESM4_ESM.csv",
            "ext_param": (True, ","),

            "samp": (False, 27),
            "p_val": (True, "F"),
            "fdr": (False, "Benjamini Hochberg"),
            "rel_strength": (True, "C"),
            "method": (False, "Log2 Fold Change From Fishers Exact Test"),

            "subj": (False, "microgravity"),
            "obj": (True, "A"),
            "pred": "biolink:affects",

            "taxon": "NCBITaxon:9606",
            "boost_cls": [
                (False, ["biolink:Gene", "biolink:OrganismTaxon"]),
            ],
        }"""),
    ),

    Example(
        input=collapse("""
            Wu
        """),
        output=collapse("""{
            "pub": "PMC:PMC11166937",
            "url": "https://pmc.ncbi.nlm.nih.gov/articles/instance/11166937/bin/41467_2023_42013_MOESM4_ESM.csv",
            "ext_param": (True, ","),

            "samp": (False, 27),
            "p_val": (True, "F"),
            "fdr": (False, "Benjamini Hochberg"),
            "rel_strength": (True, "C"),
            "method": (False, "Log2 Fold Change From Fishers Exact Test"),

            "subj": (False, "microgravity"),
            "obj": (True, "A"),
            "pred": "biolink:affects",

            "taxon": "NCBITaxon:9606",
            "boost_cls": [
                (False, ["biolink:Gene", "biolink:OrganismTaxon"]),
            ],
        }"""),
    ),

    Example(
        input=collapse("""
            Zhou
        """),
        output=collapse("""{
            "pub": "PMC:PMC9153113",
            "url": "https://pmc.ncbi.nlm.nih.gov/articles/instance/9153113/bin/40168_2022_1271_MOESM1_ESM.xls",
            "ext_param": (False, "Table S29"),
            "row_slice": (4, None),

            "fdr": (False, "Bonferroni"),
            "rel_strength": (False, "ML"),
            "method": (False, "One/Two-way-ANOVA"),

            "subj": (True, "A"),
            "obj": (False, "p-Hydroxyphenylacetic acid"),
            "pred": "biolink:correlated_with",

            "boost_cls": [
                (True, ["biolink:OrganismTaxon"]),
            ],
        }"""),
    ),

    Example(
        input=collapse("""
            Zhou
        """),
        output=collapse("""{
            "pub": "PMC:PMC9153113",
            "url": "https://pmc.ncbi.nlm.nih.gov/articles/instance/9153113/bin/40168_2022_1271_MOESM1_ESM.xls",
            "ext_param": (False, "Table S29"),
            "row_slice": (4, None),

            "fdr": (False, "Bonferroni"),
            "rel_strength": (False, "ML"),
            "method": (False, "One/Two-way-ANOVA"),

            "subj": (True, "A"),
            "obj": (False, "p-Hydroxyphenylacetic acid"),
            "pred": "biolink:correlated_with",

            "boost_cls": [
                (True, ["biolink:OrganismTaxon"]),
            ],
        }"""),
    ),

    Example(
        input=collapse("""
            Zhou
        """),
        output=collapse("""{
            "pub": "PMC:PMC9153113",
            "url": "https://pmc.ncbi.nlm.nih.gov/articles/instance/9153113/bin/40168_2022_1271_MOESM1_ESM.xls",
            "ext_param": (False, "Table S29"),
            "row_slice": (4, None),

            "fdr": (False, "Bonferroni"),
            "rel_strength": (False, "ML"),
            "method": (False, "One/Two-way-ANOVA"),

            "subj": (True, "A"),
            "obj": (False, "p-Hydroxyphenylacetic acid"),
            "pred": "biolink:correlated_with",

            "boost_cls": [
                (True, ["biolink:OrganismTaxon"]),
            ],
        }"""),
    ),

]