__author__ = "Skye Lane Goetz"

from src.qa_vector_database.utils import collapse
from langchain.schema import Example


HUMAN_CURATED_EXAMPLES: list[Example] = [
    Example(
        input=collapse(
            """
            article is PMC:PMC9691620
            use Table S3 from it
            from https://pmc.ncbi.nlm.nih.gov/articles/instance/9691620/bin/NIHMS1845232-supplement-1845232_Sup_Tab_1-5.xlsx
            these are associations
            and the subject is in column B and prioritize biolink:OrganismTaxon
            and the object is in column O
            while the p values are in F and they used a Bonferroni correction
            the sample size is 3064
            relationship strength is in column E and its a Two-sided Wald test
        """
        ),
        output=collapse(
            """{
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
        }"""
        ),
    ),
    Example(
        input=collapse(
            """
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
        """
        ),
        output=collapse(
            """{
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
        }"""
        ),
    ),
    Example(
        input=collapse(
            """
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
        """
        ),
        output=collapse(
            """{
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
        }"""
        ),
    ),
    Example(
        input=collapse(
            """
            From Fackleman et al.'s Gut microbiome signatures of vegan, vegetarian and omnivore diets and associated health outcomes across 21,561 individuals
            (PMC:PMC11726441)
            extract information from the supplemental data table 41564_2024_1870_MOESM4_ESM.xlsx (specifically sheet "Supplementary Table 13"),
            -- which you can download at https://static-content.springer.com/esm/art%3A10.1038%2Fs41564-024-01870-z/MediaObjects/41564_2024_1870_MOESM4_ESM.xlsx.
            Start at row 2 and then go read the rest of the data.
            The sample size is n = 21561 individiuals.
            P-values can be found in column G of the table; they are FDR corrected with the benjamini-hochberg multiple testing correction method.
            There is no explicit relationship strength; however, the relationships are spearman correlations.
            The triple in the paper best corresponds to biolink:associated_with.
            The triple subject can be found in column A.
            The triple object can be found in column B.
            Please don't let either the subject or object map to biolink:OrganismTaxon.
        """
        ),
        output=collapse(
            """{
            "pub": "PMC:PMC11726441",
            "url": "https://static-content.springer.com/esm/art%3A10.1038%2Fs41564-024-01870-z/MediaObjects/41564_2024_1870_MOESM4_ESM.xlsx",
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
        }"""
        ),
    ),
    Example(
        input=collapse(
            """
            The publication is PMC11726441 from pubmed
            and I want you to download https://static-content.springer.com/esm/art%3A10.1038%2Fs41564-024-01870-z/MediaObjects/41564_2024_1870_MOESM4_ESM.xlsx.
            and use sheet Supplementary Table 13.
            Start at row 2.
            sample size = 21561.
            pvalues = column G.
            multiple testing correction = Benjamini hochberg.
            assertion method = spearman correlation.
            The predicate is associated_with while the subject is in column A and the object is in column B.
            prioritize taxa for both the subject and object
        """
        ),
        output=collapse(
            """{
            "pub": "PMC:PMC11726441",
            "url": "https://static-content.springer.com/esm/art%3A10.1038%2Fs41564-024-01870-z/MediaObjects/41564_2024_1870_MOESM4_ESM.xlsx",
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
        }"""
        ),
    ),
    Example(
        input=collapse(
            """
            The pmc is 11726441
            download at https://static-content.springer.com/esm/art%3A10.1038%2Fs41564-024-01870-z/MediaObjects/41564_2024_1870_MOESM4_ESM.xlsx.
            use Supplementary Table 13.
            row 2 = start
            n = 21561.
            p = G (Benjamini Hochberg)
            method = spearman correlation.
            column A (organism taxon) is associated_with column B (organism taxon).
        """
        ),
        output=collapse(
            """{
            "pub": "PMC:PMC11726441",
            "url": "https://static-content.springer.com/esm/art%3A10.1038%2Fs41564-024-01870-z/MediaObjects/41564_2024_1870_MOESM4_ESM.xlsx",
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
        }"""
        ),
    ),
    Example(
        input=collapse(
            """
            Make a new template with this Fuess paper.
            The PMC is PMC:PMC8262870 and the download is https://pmc.ncbi.nlm.nih.gov/articles/instance/8262870/bin/mbio.00145-21-sd002.xlsx.
            Use the sheet Geodermatophilaceae and start at row 2.
            The sample size is 1929 and the relationship strength is in column D (computed using a signed network using bicor analyses).
            The subject is also Geodermatophilaceae (prioritize taxa) and the object is in column C.
            The predicate is correlated with and map everything in NCBITaxon:69293.
        """
        ),
        output=collapse(
            """{
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

            "taxon": "NCBITaxon:69293",
            "boost_cls": [
                (True, ["biolink:OrganismTaxon"]),
            ],
        }"""
        ),
    ),
    Example(
        input=collapse(
            """
            PMC:PMC8262870
            https://pmc.ncbi.nlm.nih.gov/articles/instance/8262870/bin/mbio.00145-21-sd002.xlsx
            sheet Geodermatophilaceae (start = 2)
            also object Geodermatophilaceae - prioritize taxon -
            n = 1929, strength = D, method = Signed network using bicor analyses
            also subject = C
            also predicate = correlated_with
            all in NCBITaxon:69293
        """
        ),
        output=collapse(
            """{
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

            "taxon": "NCBITaxon:69293",
            "boost_cls": [
                (True, ["biolink:OrganismTaxon"]),
            ],
        }"""
        ),
    ),
    Example(
        input=collapse(
            """
            New template (PMC8262870):
            Geodermatophilaceae ["biolink:OrganismTaxon"] is "biolink:correlated_with" column C [both in "NCBITaxon:69293"].
            Download from https://pmc.ncbi.nlm.nih.gov/articles/instance/8262870/bin/mbio.00145-21-sd002.xlsx
            and use (starting at row 2) the sheet Geodermatophilaceae.
            Sample size = 1929. P_value = None, Multiple Testing Correction = None, Assertion Strength = D, method = "Signed network using bicor analyses".
        """
        ),
        output=collapse(
            """{
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

            "taxon": "NCBITaxon:69293",
            "boost_cls": [
                (True, ["biolink:OrganismTaxon"]),
            ],
        }"""
        ),
    ),
    Example(
        input=collapse(
            """
            Lui Paper with PMC:PMC10052271. The url = https://static-content.springer.com/esm/art%3A10.1038%2Fs41598-023-31115-8/MediaObjects/41598_2023_31115_MOESM7_ESM.xlsx
            and the sheet is Supplementary Table 6, starting at 2.
            The sample size is in column L while the p is in column K and the strength is in column I. The method use for the anlayiss was a Generalised summary-data-based Mendelian randomization.
            The subject is in column h (boost organism taxon) and the predicate is affects. The objevt is the value longveity and for the mapping prioritize PhenotypicFeatures and ClinicalFindings while avoiding Genes (at all costs).
        """
        ),
        output=collapse(
            """{
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
        }"""
        ),
    ),
    Example(
        input=collapse(
            """
            The new template pmc is 10052271 and the file you can download is at
            "https://static-content.springer.com/esm/art%3A10.1038%2Fs41598-023-31115-8/MediaObjects/41598_2023_31115_MOESM7_ESM.xlsx"
            where you WILL use Supplementary Table 6 and YOU WILL start at row = 2.
            Sample = L
            P = K
            FDR = NA
            strength = column I
            method = Generalised summary-data-based Mendelian randomization
            subject = H (must be taxon)
            object = longevity (try "biolink:PhenotypicFeature", "biolink:ClinicalFinding" and avoid "biolink:Gene")
            predicate = biolink:affects
        """
        ),
        output=collapse(
            """{
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
        }"""
        ),
    ),
    Example(
        input=collapse(
            """
            Lui paper at https://static-content.springer.com/esm/art%3A10.1038%2Fs41598-023-31115-8/MediaObjects/41598_2023_31115_MOESM7_ESM.xlsx
            pmc is also "PMC:PMC10052271"
            while using sheetname = Supplementary Table 6
            and starting at 2.
            n = col L
            p is in col K
            strength=columnI
            its method is Generalised summary-data-based Mendelian randomization
            subject is col H (boost taxa)
            predicate is affects
            object is longevity (boost clinical finding and phenotypic feature from biolink) (drop gene also from biolink)?
        """
        ),
        output=collapse(
            """{
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
        }"""
        ),
    ),
    Example(
        input=collapse(
            """
            Pu https://static-content.springer.com/esm/art%3A10.1038%2Fs43587-024-00678-0/MediaObjects/43587_2024_678_MOESM12_ESM.csv is a csv
            with pubmed_id 39054372 -
            use "," as a delimiter.
            The sample size is 1448 people and the p_values are in column D for a linear regression.
            The p_values are corrected with the Benjamini-Hochberg multiple testing correction method.
            The coefficent for the linear regression is in column C.
            Subject is in col A obj is in col B and predi is associated with.
            Prioritize taxa for the subject column.
        """
        ),
        output=collapse(
            """{
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
        }"""
        ),
    ),
    Example(
        input=collapse(
            """
            https://static-content.springer.com/esm/art%3A10.1038%2Fs43587-024-00678-0/MediaObjects/43587_2024_678_MOESM12_ESM.csv from
            PMID:39054372 connects taxa in column A with column B via associations using linear regressions on a sample of 1448
            with Benjamini Hochberg fdr (p in col D, strength in col C).
        """
        ),
        output=collapse(
            """{
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
        }"""
        ),
    ),
    Example(
        input=collapse(
            """
            PMID:39054372
            https://static-content.springer.com/esm/art%3A10.1038%2Fs43587-024-00678-0/MediaObjects/43587_2024_678_MOESM12_ESM.csv
            ","
            n = 1448
            p = D
            fdr = Benjamini Hochberg
            strength = C
            method = Linear regression
            subject in A (priortize "biolink:OrganismTaxon")
            object in B
            pred = biolink:associated_with
        """
        ),
        output=collapse(
            """{
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
        }"""
        ),
    ),
    Example(
        input=collapse(
            """
            Qin made an excel sheet (PMC:PMC11401200, https://pmc.ncbi.nlm.nih.gov/articles/instance/11401200/bin/mmc3.xlsx, Sheet1)
            that connects genes in column E with genes in column B (all in taxon 9606) using associated_with_resistance_to
            with a LASSO Regression from the first row of the sheet to row 200k (200_000). The regression was preformed with a sample
            of 969 and the coeffiecents are in column C
        """
        ),
        output=collapse(
            """{
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
        }"""
        ),
    ),
    Example(
        input=collapse(
            """
            In humans (NCBITaxon 9606) the publication PMC:PMC11401200 has an excel downloadable at https://pmc.ncbi.nlm.nih.gov/articles/instance/11401200/bin/mmc3.xlsx
            who's Sheet1 for the first 200000 rows connects human genes in column E with human genes in column B with the predicate biolink:associated_with_resistance_to
            through a lasso regression (n=969, coeffs in column C)
        """
        ),
        output=collapse(
            """{
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
        }"""
        ),
    ),
    Example(
        input=collapse(
            """
            prioritize biolink:Gene for both subject and object
            predicate is associated_with_resistance_to
            n-969, strength=C for LASSO regression.
            subject and object are in the model NCBITaxon:9606.
            url for download at https://pmc.ncbi.nlm.nih.gov/articles/instance/11401200/bin/mmc3.xlsx
            - use end at row 200,000 of Sheet1.
            object in col B, subject col E
        """
        ),
        output=collapse(
            """{
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
        }"""
        ),
    ),
    Example(
        input=collapse(
            """
            I want a new template I'll add sections to from a supplemental data mr chet gepetit.
            My paprer is PMC:PMC10434204 and I want you to donwload the hyper uber important critical
            supplemental table at https://pmc.ncbi.nlm.nih.gov/articles/instance/10434204/bin/spectrum.03429-22-s0001.xlsx.
            WEIRD_ khfsydfgi v,jh Unrelated Ghgsydgy Rambling :3.
            From this amazing table I want you to use SupplementalTable_3 from ROW 3 onward and ONLY row 3 onward my geptiti friend.
            ANOTHER WEIRD RAMBLING CONVERSATION ABOUT QUEEN ELIZABETH IV.
            The sample size for this crutial work is 474 and this was feed to a LME model.
            P_values were FRD corrected with an unspecified method at 10% and are in column H.
            The assertion strength is in hyper important (SURPRISE TANGENT) column E.
            The subject is in the beautiful engligh column of cornwall, sorry I mean the subject is overriden and in the literal column B (obj=D).
            The predicate is column associated_with and boost the almighty holy organism taxon for both object and subject.
        """
        ),
        output=collapse(
            """{
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
        }"""
        ),
    ),
    Example(
        input=collapse(
            """
            Romero has a paper in pubmed central that is PMC:PMC10434204 with a file at URL https://pmc.ncbi.nlm.nih.gov/articles/instance/10434204/bin/spectrum.03429-22-s0001.xlsx
            this file has a table of SupplementalTable_3 that starting at row #5 connectes taxa in column B with taxa in column D through associations with eachother.
            This was done using an LME model with an FDR of 10 percent on a cohort of 474. The pvalue is in H while the relationship strength is in column E.
        """
        ),
        output=collapse(
            """{
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
        }"""
        ),
    ),
    Example(
        input=collapse(
            """
            Romero = PMC:PMC10434204
            location: https://pmc.ncbi.nlm.nih.gov/articles/instance/10434204/bin/spectrum.03429-22-s0001.xlsx @ SupplementalTable_3 [5:]
            n=474
            p=colH
            fdr=FDR of 10 percent
            rel_strength=colE
            method is an LME model
            subject: colB
            obj: colD
            pred: associated_with
            prioritize biolink:OrganismTaxon node wide
            do not avoid any biolink:Category node-wide
        """
        ),
        output=collapse(
            """{
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
        }"""
        ),
    ),
]

HUMAN_VALIDATED_GPT_o4_MINI_HIGH_CURATED_EXAMPLES: list[Example] = [
    Example(
        input=collapse(
            """
            From Wang et al.'s study on T helper cell differentiation (PMC:PMC6555748),
            download the supplemental Excel at https://pmc.ncbi.nlm.nih.gov/articles/instance/6555748/bin/12931_2019_1085_MOESM5_ESM.xlsx.
            Use sheet "A. Th1 and Th2 pathway" starting at row 3.
            Sample size = 59.
            P-values are in column C (Benjamini Hochberg).
            Relationship strength in column D via Spearman correlation.
            Subject in column A; object is Haemophilus.
            All entries map to NCBITaxon:9606.
            Boost genes; drop proteins.
            Predicate: biolink:associated_with.
        """
        ),
        output=collapse(
            """{
            "pub": "PMC:PMC6555748",
            "url": "https://pmc.ncbi.nlm.nih.gov/articles/instance/6555748/bin/12931_2019_1085_MOESM5_ESM.xlsx",
            "ext_param": (False, "A. Th1 and Th2 pathway"),
            "row_slice": (3, None),

            "samp": (False, 59),
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
            ],
            "drop_cls": [
                (True, ["biolink:Protein"]),
            ],
        }"""
        ),
    ),
    Example(
        input=collapse(
            """
            Wang PMC6555748 excel sheet T helper:
            https://pmc.ncbi.nlm.nih.gov/articles/instance/6555748/bin/12931_2019_1085_MOESM5_ESM.xlsx,
            use sheet A. Th1 and Th2 pathway @ row 3.
            n = 59; p = C (FDR BH); strength = D; method = Spearman;
            subj=A; obj=Haemophilus; taxon 9606; predicate associated_with;
            prioritize gene; avoid protein.
        """
        ),
        output=collapse(
            """{
            "pub": "PMC:PMC6555748",
            "url": "https://pmc.ncbi.nlm.nih.gov/articles/instance/6555748/bin/12931_2019_1085_MOESM5_ESM.xlsx",
            "ext_param": (False, "A. Th1 and Th2 pathway"),
            "row_slice": (3, None),

            "samp": (False, 59),
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
            ],
            "drop_cls": [
                (True, ["biolink:Protein"]),
            ],
        }"""
        ),
    ),
    Example(
        input=collapse(
            """
            Wang et al. T helper pathways (PMC:PMC6555748):
            Download at https://pmc.ncbi.nlm.nih.gov/articles/instance/6555748/bin/12931_2019_1085_MOESM5_ESM.xlsx,
            sheet A. Th1 and Th2 pathway, start row 3.
            Cohort of 59.
            Column C holds p-values (BH); column D the Spearman rho.
            Map subjects A and objects Haemophilus to human (9606).
            Boost Gene class; drop Protein.
        """
        ),
        output=collapse(
            """{
            "pub": "PMC:PMC6555748",
            "url": "https://pmc.ncbi.nlm.nih.gov/articles/instance/6555748/bin/12931_2019_1085_MOESM5_ESM.xlsx",
            "ext_param": (False, "A. Th1 and Th2 pathway"),
            "row_slice": (3, None),

            "samp": (False, 59),
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
            ],
            "drop_cls": [
                (True, ["biolink:Protein"]),
            ],
        }"""
        ),
    ),
    Example(
        input=collapse(
            """
            Wu et al. microgravity effects (PMC:PMC11166937):
            File: https://pmc.ncbi.nlm.nih.gov/articles/instance/11166937/bin/41467_2023_42013_MOESM4_ESM.csv (CSV, default comma).
            Start at first row.
            Sample size 27.
            P in column F (Benjamini Hochberg); rel strength in C.
            Method: Log2 fold change from Fisher's exact test.
            Subject literal "microgravity"; object in A.
            Map all to NCBITaxon:9606.
            Predicate: biolink:affects.
            Boost both Gene and OrganismTaxon.
        """
        ),
        output=collapse(
            """{
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
        }"""
        ),
    ),
    Example(
        input=collapse(
            """
            From Zhou et al. metabolite correlations (PMC:PMC9153113),
            download XLS from https://pmc.ncbi.nlm.nih.gov/articles/instance/9153113/bin/40168_2022_1271_MOESM1_ESM.xls.
            Table S29, start at row 4.
            No p-values reported; FDR Bonferroni applies.
            No explicit strength column (ML used).
            Analysis via one/two-way ANOVA.
            Subject in A; object p-Hydroxyphenylacetic acid.
            Predicate: biolink:correlated_with.
            Boost OrganismTaxon.
        """
        ),
        output=collapse(
            """{
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
        }"""
        ),
    ),
    Example(
        input=collapse(
            """
            PMID:12345678
            https://example.com/data_table.tsv
            delimiter = "\t"
            sheet not applicable
            start row = 2, end row = 100
            sample size present in column 5
            p-values = column 6 (none correction)
            strength = column 7 (no test specified)
            subject = column 1
            object = column 2
            predicate = biolink:related_to
            boost PhenotypicFeature, drop Gene.
        """
        ),
        output=collapse(
            """{
            "pub": "PMID:12345678",
            "url": "https://example.com/data_table.tsv",
            "ext_param": (True, "\t"),
            "row_slice": (2, 100),

            "samp": (True, "5"),
            "p_val": (True, "6"),
            "rel_strength": (True, "7"),
            "method": (False, ""),

            "subj": (True, "1"),
            "obj": (True, "2"),
            "pred": "biolink:related_to",

            "boost_cls": [
                (False, ["biolink:PhenotypicFeature"]),
            ],
            "drop_cls": [
                (False, ["biolink:Gene"]),
            ],
        }"""
        ),
    ),
    Example(
        input=collapse(
            """
            PMC:PMC9999999
            https://example.org/results.csv
            default comma
            sheet irrelevant
            no sample size stated
            no p-values; only FDR reported as q-values in column D
            relationship strength = None
            method = permutation test
            subject = treatment A
            object = outcome B
            predicate = biolink:impacts
            boost ClinicalFinding.
        """
        ),
        output=collapse(
            """{
            "pub": "PMC:PMC9999999",
            "url": "https://example.org/results.csv",
            "ext_param": (True, ","),

            "fdr": (False, "q-values in D"),
            "method": (False, "permutation test"),

            "subj": (False, "treatment A"),
            "obj": (False, "outcome B"),
            "pred": "biolink:impacts",

            "boost_cls": [
                (False, ["biolink:ClinicalFinding"]),
            ],
        }"""
        ),
    ),
    Example(
        input=collapse(
            """
            PMID:22222222 supplemental macro file:
            https://data.example.net/supplement.xlsm
            sheet MacroData (rows 10 to 500)
            n = col Z
            p = col Y (Bonferroni)
            strength = col X
            method = mixed-effects model
            subj = column A
            obj = column B
            pred = biolink:modulates
            taxon = NCBITaxon:10090
            boost OrganismTaxon, drop ChemicalEntity.
        """
        ),
        output=collapse(
            """{
            "pub": "PMID:22222222",
            "url": "https://data.example.net/supplement.xlsm",
            "ext_param": (False, "MacroData"),
            "row_slice": (10, 500),

            "samp": (True, "Z"),
            "p_val": (True, "Y"),
            "fdr": (False, "Bonferroni"),
            "rel_strength": (True, "X"),
            "method": (False, "mixed-effects model"),

            "subj": (True, "A"),
            "obj": (True, "B"),
            "pred": "biolink:modulates",

            "taxon": "NCBITaxon:10090",
            "boost_cls": [
                (False, ["biolink:OrganismTaxon"]),
            ],
            "drop_cls": [
                (False, ["biolink:ChemicalEntity"]),
            ],
        }"""
        ),
    ),
    Example(
        input=collapse(
            """
            Publication PMC:PMC7000123
            download https://pmc.ncbi.nlm.nih.gov/articles/instance/7000123/bin/data_fig2.xlsx
            use sheet Fig2Data
            start at row 1
            sample size = 120
            p-values in column C
            no multiple testing correction
            relationship strength = column D
            method = Student's t-test
            subject = column A
            object = column E (ChemicalEntity)
            predicate = biolink:associated_with
            boost ChemicalEntity; drop Pathway
        """
        ),
        output=collapse(
            """{
            "pub": "PMC:PMC7000123",
            "url": "https://pmc.ncbi.nlm.nih.gov/articles/instance/7000123/bin/data_fig2.xlsx",
            "ext_param": (False, "Fig2Data"),
            "row_slice": (1, None),

            "samp": (False, 120),
            "p_val": (True, "C"),
            "rel_strength": (True, "D"),
            "method": (False, "Student's t-test"),

            "subj": (True, "A"),
            "obj": (True, "E"),
            "pred": "biolink:associated_with",

            "boost_cls": [
                (True, ["biolink:ChemicalEntity"]),
            ],
            "drop_cls": [
                (False, ["biolink:Pathway"]),
            ],
        }"""
        ),
    ),
    Example(
        input=collapse(
            """
            PMC:PMC8888888
            https://data.server.com/table.tsv
            default TSV delimiter
            sheet irrelevant
            start = 3
            sample = 200
            p-values = col P (FDR Benjamini-Hochberg)
            strength = col R
            no method specified
            subject in col X
            object = Y
            pred = biolink:affects
            boost OrganismTaxon
        """
        ),
        output=collapse(
            """{
            "pub": "PMC:PMC8888888",
            "url": "https://data.server.com/table.tsv",
            "ext_param": (True, "\t"),
            "row_slice": (3, None),

            "samp": (False, 200),
            "p_val": (True, "P"),
            "fdr": (False, "Benjamini Hochberg"),
            "rel_strength": (True, "R"),

            "subj": (True, "X"),
            "obj": (False, "Y"),
            "pred": "biolink:affects",

            "boost_cls": [
                (True, ["biolink:OrganismTaxon"]),
            ],
        }"""
        ),
    ),
    Example(
        input=collapse(
            """
            PMID:33333333 supplementary xls:
            https://ftp.example.net/data/supplement.xls
            sheet DataSheet
            sample size in header row
            pvalues in column B
            FDR = None
            strength = column C
            method = chi-square test
            subj = column A cells
            obj = column D cells
            pred = biolink:correlated_with
            boost PhenotypicFeature
            drop Taxon
        """
        ),
        output=collapse(
            """{
            "pub": "PMID:33333333",
            "url": "https://ftp.example.net/data/supplement.xls",
            "ext_param": (False, "DataSheet"),

            "p_val": (True, "B"),
            "rel_strength": (True, "C"),
            "method": (False, "chi-square test"),

            "subj": (True, "A"),
            "obj": (True, "D"),
            "pred": "biolink:correlated_with",

            "boost_cls": [
                (False, ["biolink:PhenotypicFeature"]),
            ],
            "drop_cls": [
                (False, ["biolink:Taxon"]),
            ],
        }"""
        ),
    ),
    Example(
        input=collapse(
            """
            From PMID:44444444 macro workbook:
            https://files.example.com/exp_data.xlsm
            sheet MacroResults rows 10-500
            sample = col M
            p = col N (Holm)
            strength = col O
            method = mixed-effects model
            subj = column E
            obj = column F
            pred = biolink:modulates
            taxon = NCBITaxon:10116
            boost OrganismTaxon; drop ChemicalEntity
        """
        ),
        output=collapse(
            """{
            "pub": "PMID:44444444",
            "url": "https://files.example.com/exp_data.xlsm",
            "ext_param": (False, "MacroResults"),
            "row_slice": (10, 500),

            "samp": (True, "M"),
            "p_val": (True, "N"),
            "fdr": (False, "Holm"),
            "rel_strength": (True, "O"),
            "method": (False, "mixed-effects model"),

            "subj": (True, "E"),
            "obj": (True, "F"),
            "pred": "biolink:modulates",

            "taxon": "NCBITaxon:10116",
            "boost_cls": [
                (True, ["biolink:OrganismTaxon"]),
            ],
            "drop_cls": [
                (False, ["biolink:ChemicalEntity"]),
            ],
        }"""
        ),
    ),
    Example(
        input=collapse(
            """
            PMID:66666666
            http://data.test.org/measurements.xlsx
            sheet Measurements
            rows 2 to 250
            no sample size specified
            p-values not provided
            fdr = q-values in col G
            strength = col H
            method = permutation test
            subj=A
            obj=B
            pred=biolink:impacts
            boost PhenotypicFeature
        """
        ),
        output=collapse(
            """{
            "pub": "PMID:66666666",
            "url": "http://data.test.org/measurements.xlsx",
            "ext_param": (False, "Measurements"),
            "row_slice": (2, 250),

            "fdr": (False, "q-values in G"),
            "rel_strength": (True, "H"),
            "method": (False, "permutation test"),

            "subj": (False, "A"),
            "obj": (False, "B"),
            "pred": "biolink:impacts",

            "boost_cls": [
                (False, ["biolink:PhenotypicFeature"]),
            ],
        }"""
        ),
    ),
    Example(
        input=collapse(
            """
            PMC:PMC7777777 ftp://ftp.example.org/exp/data.csv
            default comma
            start=1
            sample=150
            p=col3
            fdr=None
            strength=None
            method=ANOVA
            subj=geneX
            obj=treatmentY
            pred=biolink:modulates
            boost Gene
        """
        ),
        output=collapse(
            """{
            "pub": "PMC:PMC7777777",
            "url": "ftp://ftp.example.org/exp/data.csv",
            "ext_param": (True, ","),
            "row_slice": (1, None),

            "samp": (False, 150),
            "p_val": (True, "C"),
            "fdr": (False, None),
            "rel_strength": (False, None),
            "method": (False, "ANOVA"),

            "subj": (False, "geneX"),
            "obj": (False, "treatmentY"),
            "pred": "biolink:modulates",

            "boost_cls": [
                (True, ["biolink:Gene"]),
            ],
        }"""
        ),
    ),
    Example(
        input=collapse(
            """
            Publication PMID:77788899
            https://files.test.com/info.xlsx
            use sheet "Study Data 2025"
            start at 4
            n=500
            p=K (Benjamini-Hochberg)
            strength=L
            method=linear model
            subj=M
            obj=N
            pred=biolink:related_to
            boost ClinicalFinding, Protein
        """
        ),
        output=collapse(
            """{
            "pub": "PMID:77788899",
            "url": "https://files.test.com/info.xlsx",
            "ext_param": (False, "Study Data 2025"),
            "row_slice": (4, None),

            "samp": (False, 500),
            "p_val": (True, "K"),
            "fdr": (False, "Benjamini Hochberg"),
            "rel_strength": (True, "L"),
            "method": (False, "linear model"),

            "subj": (True, "M"),
            "obj": (True, "N"),
            "pred": "biolink:related_to",

            "boost_cls": [
                (False, ["biolink:ClinicalFinding", "biolink:Protein"]),
            ],
        }"""
        ),
    ),
    Example(
        input=collapse(
            """
            PMC:PMC8880001
            https://data.host.org/genomics.csv
            default delimiter
            no sheet
            no row info
            sample=1000
            pvalues in col 10
            fdr=Benjamini-Hochberg
            strength in col 11
            method=Bayesian regression
            subj=A
            obj=B
            pred=biolink:interacts_with
            boost OrganismTaxon
        """
        ),
        output=collapse(
            """{
            "pub": "PMC:PMC8880001",
            "url": "https://data.host.org/genomics.csv",
            "ext_param": (True, ","),

            "samp": (False, 1000),
            "p_val": (True, "J"),
            "fdr": (False, "Benjamini Hochberg"),
            "rel_strength": (True, "K"),
            "method": (False, "Bayesian regression"),

            "subj": (False, "A"),
            "obj": (False, "B"),
            "pred": "biolink:interacts_with",

            "boost_cls": [
                (True, ["biolink:OrganismTaxon"]),
            ],
        }"""
        ),
    ),
    Example(
        input=collapse(
            """
            PMID:99900011
            https://research.org/data/set.xlsx
            sheet Main
            start row 2
            no n provided
            p in column D
            FDR of 5%
            rel strength = column E
            method = Spearman correlation
            subj = column A
            obj = "treatment effect"
            pred = biolink:causes
            boost PhenotypicFeature
            drop OrganismTaxon
        """
        ),
        output=collapse(
            """{
            "pub": "PMID:99900011",
            "url": "https://research.org/data/set.xlsx",
            "ext_param": (False, "Main"),
            "row_slice": (2, None),

            "p_val": (True, "D"),
            "fdr": (False, "FDR of 5%"),
            "rel_strength": (True, "E"),
            "method": (False, "Spearman correlation"),

            "subj": (True, "A"),
            "obj": (False, "treatment effect"),
            "pred": "biolink:causes",

            "boost_cls": [
                (False, ["biolink:PhenotypicFeature"]),
            ],
            "drop_cls": [
                (False, ["biolink:OrganismTaxon"]),
            ],
        }"""
        ),
    ),
    Example(
        input=collapse(
            """
            PMID:13131313 xlsx at https://files.test.org/data.xlsx sheet Complex
            start=3
            n=250
            p=A (Bonferroni)
            strength=B
            method=multiple regression
            subj=C
            obj=D
            pred=biolink:modifies
            boost OrganismTaxon then Gene
            drop ChemicalEntity then Pathway
        """
        ),
        output=collapse(
            """{
            "pub": "PMID:13131313",
            "url": "https://files.test.org/data.xlsx",
            "ext_param": (False, "Complex"),
            "row_slice": (3, None),

            "samp": (False, 250),
            "p_val": (True, "A"),
            "fdr": (False, "Bonferroni"),
            "rel_strength": (True, "B"),
            "method": (False, "multiple regression"),

            "subj": (True, "C"),
            "obj": (True, "D"),
            "pred": "biolink:modifies",

            "boost_cls": [
                (False, ["biolink:OrganismTaxon"]),
                (True, ["biolink:Gene"]),
            ],
            "drop_cls": [
                (False, ["biolink:ChemicalEntity"]),
                (False, ["biolink:Pathway"]),
            ],
        }"""
        ),
    ),
    Example(
        input=collapse(
            """
            PMC:PMC2222111 https://host.org/info.csv default comma
            start row 10
            n in col Z
            p in col Y
            FDR none
            strength col X
            method Random Forest
            subj col A
            obj col B
            pred=biolink:related_to
            boost OrganismTaxon
        """
        ),
        output=collapse(
            """{
            "pub": "PMC:PMC2222111",
            "url": "https://host.org/info.csv",
            "ext_param": (True, ","),
            "row_slice": (10, None),

            "samp": (True, "Z"),
            "p_val": (True, "Y"),
            "fdr": (False, None),
            "rel_strength": (True, "X"),
            "method": (False, "Random Forest"),

            "subj": (True, "A"),
            "obj": (True, "B"),
            "pred": "biolink:related_to",

            "boost_cls": [
                (True, ["biolink:OrganismTaxon"]),
            ],
        }"""
        ),
    ),
    Example(
        input=collapse(
            """
            PMID:14141414 file at https://sci.org/dataset.xlsx
            sheet name = "RESULTS_Summary"
            start row 2
            n=80
            p values col H
            FDR BH
            strength col I
            method = Kaplan-Meier
            subj col J
            obj col K
            pred=biolink:impacts
            boost ClinicalFinding
        """
        ),
        output=collapse(
            """{
            "pub": "PMID:14141414",
            "url": "https://sci.org/dataset.xlsx",
            "ext_param": (False, "RESULTS_Summary"),
            "row_slice": (2, None),

            "samp": (False, 80),
            "p_val": (True, "H"),
            "fdr": (False, "Benjamini Hochberg"),
            "rel_strength": (True, "I"),
            "method": (False, "Kaplan-Meier"),

            "subj": (True, "J"),
            "obj": (True, "K"),
            "pred": "biolink:impacts",

            "boost_cls": [
                (True, ["biolink:ClinicalFinding"]),
            ],
        }"""
        ),
    ),
    Example(
        input=collapse(
            """
            PMC:PMC3131313 https://repo.org/data.xls sheet DataMix
            start row 5
            sample = 300
            p = col M (none)
            strength = col N
            method = chi-square
            subj = col O
            obj = col P
            pred = biolink:correlated_with
            boost PhenotypicFeature
        """
        ),
        output=collapse(
            """{
            "pub": "PMC:PMC3131313",
            "url": "https://repo.org/data.xls",
            "ext_param": (False, "DataMix"),
            "row_slice": (5, None),

            "samp": (False, 300),
            "p_val": (True, "M"),
            "fdr": (False, None),
            "rel_strength": (True, "N"),
            "method": (False, "chi-square"),

            "subj": (True, "O"),
            "obj": (True, "P"),
            "pred": "biolink:correlated_with",

            "boost_cls": [
                (True, ["biolink:PhenotypicFeature"]),
            ],
        }"""
        ),
    ),
    Example(
        input=collapse(
            """
            PMID:15151515 file.csv delimiter=COMMA start=1
            n=50
            p=col A
            fdr None
            strength=col B
            method t-test
            subj col C
            obj col D
            pred biolink:associated_with
            boost Protein
        """
        ),
        output=collapse(
            """{
            "pub": "PMID:15151515",
            "url": "file.csv",
            "ext_param": (True, ","),
            "row_slice": (1, None),

            "samp": (False, 50),
            "p_val": (True, "A"),
            "fdr": (False, None),
            "rel_strength": (True, "B"),
            "method": (False, "t-test"),

            "subj": (True, "C"),
            "obj": (True, "D"),
            "pred": "biolink:associated_with",

            "boost_cls": [
                (True, ["biolink:Protein"]),
            ],
        }"""
        ),
    ),
    Example(
        input=collapse(
            """
            PMC:PMC16161616 https://data.alpha.org/🧬_sheet.xlsx
            sheet "Data 🧬"
            start row 6
            n=42
            p-col=G
            fdr=Benjamini
            strength=H
            method=Fisher's exact
            subj=I
            obj=J
            pred=biolink:coexists_with
            boost OrganismTaxon
        """
        ),
        output=collapse(
            """{
            "pub": "PMC:PMC16161616",
            "url": "https://data.alpha.org/🧬_sheet.xlsx",
            "ext_param": (False, "Data 🧬"),
            "row_slice": (6, None),

            "samp": (False, 42),
            "p_val": (True, "G"),
            "fdr": (False, "Benjamini"),
            "rel_strength": (True, "H"),
            "method": (False, "Fisher's exact"),

            "subj": (True, "I"),
            "obj": (True, "J"),
            "pred": "biolink:coexists_with",

            "boost_cls": [
                (True, ["biolink:OrganismTaxon"]),
            ],
        }"""
        ),
    ),
    Example(
        input=collapse(
            """
            PMID:17171717 https://data.mix.org/mix.xlsx
            sheet mixedCASE
            start row 8
            n=88
            p=col L
            fdr=None
            strength=M
            method=Poisson regression
            subj=col N
            obj=col O
            pred=biolink:affects
            boost Gene
        """
        ),
        output=collapse(
            """{
            "pub": "PMID:17171717",
            "url": "https://data.mix.org/mix.xlsx",
            "ext_param": (False, "mixedCASE"),
            "row_slice": (8, None),

            "samp": (False, 88),
            "p_val": (True, "L"),
            "rel_strength": (True, "M"),
            "method": (False, "Poisson regression"),

            "subj": (True, "N"),
            "obj": (True, "O"),
            "pred": "biolink:affects",

            "boost_cls": [
                (True, ["biolink:Gene"]),
            ],
        }"""
        ),
    ),
]

EXAMPLES: list[Example] = (
    HUMAN_CURATED_EXAMPLES + HUMAN_VALIDATED_GPT_o4_MINI_HIGH_CURATED_EXAMPLES
)
