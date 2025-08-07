from transformers import AutoTokenizer, AutoModel, AutoModelForCausalLM, pipeline  # type: ignore
from src.table_config_agent.core.llms import from_transformers, set_seed
from src.table_config_agent.chroma_db.build import HuggingFaceEmbeddings
from src.table_config_agent.models.slim_cfg import SectionConfigSlim
from src.table_config_agent.core.utils import collapse, load_model
from langchain_core.runnables import Runnable, RunnableLambda
from langchain.output_parsers import PydanticOutputParser
from langchain_huggingface import HuggingFacePipeline
from langchain.prompts import PromptTemplate
from langchain_chroma import Chroma
from ast import literal_eval
from pprint import pprint
from pathlib import Path
from typing import Any
import re


def transformers_pipeline(
    tokenizer: AutoTokenizer, pipeline_model: AutoModelForCausalLM
) -> HuggingFacePipeline:
    return HuggingFacePipeline(
        pipeline=pipeline(  # type: ignore
            "text-generation",  # deepseek-coder doesn't support the other modes
            tokenizer=tokenizer,
            model=pipeline_model,
            do_sample=False,
            temperature=0.0,  # I have to explicitly specify this to stop it from autofilling to 0.7 and throwing an error
            max_new_tokens=512,
            repetition_penalty=1.2,
            return_full_text=False,
        )
    )


def chroma_db_fewshots(
    tokenizer: AutoTokenizer,
    embedding_model: AutoModel,
    chroma_p: Path,
    user_input: str,
    k: int,
) -> list[Any]:
    chroma_db: str = chroma_p.as_posix()
    db = Chroma(
        persist_directory=chroma_db,
        embedding_function=HuggingFaceEmbeddings(tokenizer, embedding_model),
        collection_name="template_examples",
    )
    fewshots = db.similarity_search(query=user_input, k=8)
    return [doc.metadata["formatted"] for doc in fewshots]


def agent_prompt() -> PromptTemplate:
    return PromptTemplate.from_template(
        """\
You are a Python dictionary generation assistant. Your task is to convert structured natural language
descriptions of tabular metadata into strictly valid Python dictionaries that match the provided schema exactly.

Each input describes:
- the publication source (e.g., PMC ID)
- the tabular file location
- how specific columns map to fields (e.g., p-value, subject, object)
- optional enhancements such as boost classes or taxonomic context

You MUST respond with:
- A single Python dictionary
- Fully valid Python (parsable by `ast.literal_eval`)
- Matching the schema structure and field types precisely

Output Schema (for reference only — do NOT include it in your output):
{pydantic_model}

Output Rules:
- Respond ONLY with the dictionary — no explanations, no markdown, no formatting
- Use double quotes for all dictionary keys
- Use double quotes for all string values
- Use True / False (capitalized) for booleans
- Use None for missing or null values
- Use (True, "A") if the field maps to a column
- Use (False, "value") or (False, value) if the field is a fixed constant
- Use lists for any collection-type fields
- Do not use markdown, code blocks, or JSON
- Do not use single quotes — always use double quotes for keys and string values

Here are example inputs and their corresponding valid Python dictionary outputs:
{fewshots}

Now generate the dictionary for the following input:
{user_input}
"""
    )


def retry_prompt() -> PromptTemplate:
    return PromptTemplate.from_template(
        """\
Your previous output was NOT valid Python and could not be interpreted as a dictionary.

You must now fix the output and re-emit ONLY a valid Python dictionary.

### DO NOT:
- Include any text before or after the dictionary (e.g., 'Answer:', 'Here is the result:', etc.)
- Use markdown formatting (e.g., triple backticks, `python`, etc.)
- Include any explanation or comments
- Include fields or values not present in the schema

### DO:
- Return a clean Python dictionary only — no preamble, no markdown, no explanation
- Use standard Python syntax:
  - Double quotes for all dictionary keys
  - Double quotes for all string values
  - Capitalized True, False, and None values
  - Use tuples like (True, "A") or (False, "value")
  - Use lists where appropriate
- Match the structure and types of the schema exactly
- Ensure the entire response is valid Python dictionary syntax (e.g., can be parsed by ast.literal_eval)

### Parsing Error:
{error_message}

### Your Invalid Output:
{bad_output}

### Python Schema (reference only — do NOT include in your output):
{pydantic_model}
"""
    )


def parse_to_dict(raw_text: str) -> dict[str, Any]:
    cleaned: str = collapse(raw_text)
    matches = re.search(r"(\{.*\})", cleaned)
    if not matches:
        msg: str = f"CODE:8 | No dict-like block found in text {cleaned}"
        raise RuntimeError(msg)
    block: str = matches.group(1)
    block = block.replace("“", '"').replace("”", '"')
    block = block.replace("‘", "'").replace("’", "'")
    block = re.sub(r"\bnull\b", "None", block, flags=re.IGNORECASE)
    block = re.sub(r"\btrue\b", "True", block, flags=re.IGNORECASE)
    block = re.sub(r"\bfalse\b", "False", block, flags=re.IGNORECASE)
    block = re.sub(r",\s*([}\]])", r"\1", block)
    try:
        return literal_eval(block)  # type: ignore
    except Exception as e:
        err: str = str(e)
        msg = f"CODE:9 | Failed to parse {block} | {err}"
        raise RuntimeError(msg)


def build_chain(cfg: dict[str, Any]) -> Runnable:  # type: ignore
    set_seed(cfg["seed"])
    tokenizer, embeding_model, pipeline_model = from_transformers(
        cfg["from_transformers"], cfg["offload_folder"]
    )
    pipe = transformers_pipeline(tokenizer, pipeline_model)
    _ = pipe.invoke("Hai")  # reduces latency for actual runs
    parser = PydanticOutputParser(pydantic_object=SectionConfigSlim)
    pydantic_model: str = parser.get_format_instructions()

    def format_agent_prompt(user_input: str) -> str:
        fewshots = chroma_db_fewshots(
            tokenizer,
            embeding_model,
            cfg["using_chroma_db"],
            user_input,
            cfg["fewshot_count"],
        )
        fewshot_str = "\n".join(fewshots)
        return agent_prompt().format(
            pydantic_model=pydantic_model, fewshots=fewshot_str, user_input=user_input
        )

    def format_retry_prompt(error_message: str, bad_output: str) -> str:
        return retry_prompt().format(
            error_message=error_message,
            bad_output=bad_output,
            pydantic_model=pydantic_model,
        )

    def invoke_with_retry(user_input: str) -> SectionConfigSlim:
        initial_prompt: str = format_agent_prompt(user_input)
        initial_raw: str = pipe.invoke(initial_prompt)

        pprint(initial_prompt)
        print("\n\n")
        pprint(initial_raw)
        print("\n\n")

        try:
            pprint(parse_to_dict(initial_raw))
            print("\n\n")
            return load_model(parse_to_dict(initial_raw), SectionConfigSlim)  # type: ignore
        except Exception as e:
            error_message: str = str(e)
            assert isinstance(initial_raw, str)
            retry_prompt: str = format_retry_prompt(error_message, initial_raw)
            retry_raw: str = pipe.invoke(retry_prompt)

            pprint(retry_prompt)
            print("\n\n")
            pprint(retry_raw)
            print("\n\n")

            try:
                pprint(parse_to_dict(retry_raw))
                print("\n\n")
                return load_model(parse_to_dict(retry_raw), SectionConfigSlim)  # type: ignore
            except Exception as e:
                assert isinstance(retry_raw, str)
                retry_error_message: str = str(e)
                msg: str = (
                    f"CODE:7 | Failed to generate a valid output | {retry_raw} | {retry_error_message}"
                )
                raise RuntimeError(msg)

    return RunnableLambda(invoke_with_retry)
