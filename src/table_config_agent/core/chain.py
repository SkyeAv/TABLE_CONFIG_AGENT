from transformers import AutoTokenizer, AutoModel, AutoModelForCausalLM, pipeline  # type: ignore
from src.table_config_agent.core.llms import from_transformers, set_seed
from src.table_config_agent.chroma_db.build import HuggingFaceEmbeddings
from src.table_config_agent.models.slim_cfg import SectionConfigSlim
from langchain_core.runnables import Runnable, RunnableLambda
from langchain.output_parsers import PydanticOutputParser
from langchain_huggingface import HuggingFacePipeline
from langchain.prompts import PromptTemplate
from langchain_chroma import Chroma
from pathlib import Path
from typing import Any


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
            max_new_tokens=1024,
            repetition_penalty=1.2,
            return_full_text=False,
        )
    )


def chroma_db_fewshots(
    tokenizer: AutoTokenizer,
    embedding_model: AutoModel,
    chroma_p: Path,
    user_input: str,
    k: int = 8,
) -> list[Any]:
    chroma_db: str = chroma_p.as_posix()
    db = Chroma(
        persist_directory=chroma_db,
        embedding_function=HuggingFaceEmbeddings(tokenizer, embedding_model),
        collection_name="template_examples",
    )
    fewshots = db.similarity_search(query=user_input, k=8)
    return [doc.formatted for doc in fewshots]  # type: ignore


def agent_prompt() -> PromptTemplate:
    # BE CONCIOUS OF NEWLINES AND SPACING FOR THE FINAL PROMPT!!
    return PromptTemplate.from_template(
        """\
You are a code generation assistant that parses text into structured configurations.

Each input describes metadata about a tabular file, including:
- the publication source
- the file location
- what columns correspond to what fields (e.g., p-values, subjects, etc.)
- optional enhancements like boosting classes or taxonomic IDs

Your job is to convert this into a valid JSON object that conforms to the given schema.

### Output Schema
{pydantic_model}

### Rules:
- Every output must be **valid JSON**
- Return a dictionary matching the schema exactly
- If a value is a column name, mark the flag as `true` and give the column letter
- If a value is fixed/constant, mark the flag as `false` and give the literal value
- If a value is missing or optional, use `null`, `None`, or the default if specified
- Never include extra text or explanations—only the JSON

You will now see several examples. Follow their format exactly.
{fewshots}

### New Input
{user_input}
"""
    )


def retry_prompt() -> PromptTemplate:
    return PromptTemplate.from_template(
        """\
Your last output was invalid JSON. Please fix the formatting and re-emit a valid response.

### Error Details:
{error_message}

### Original Output:
{bad_output}

### JSON Schema Instructions:
{pydantic_model}
"""
    )


def build_chain(cfg: dict[str, Any]) -> Runnable:  # type: ignore
    set_seed(cfg["seed"])
    tokenizer, embeding_model, pipeline_model = from_transformers(
        cfg["from_transformers"]
    )
    pipe = transformers_pipeline(tokenizer, pipeline_model)
    _ = pipe.invoke("Hai")  # reduces latency for actual runs
    parser = PydanticOutputParser(pydantic_object=SectionConfigSlim)
    pydantic_model: str = parser.get_format_instructions()

    def format_agent_prompt(user_input: str) -> str:
        fewshots = chroma_db_fewshots(
            tokenizer, embeding_model, cfg["using_chroma_db"], user_input
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
        initial_raw: str = pipe.invoke(initial_prompt)[0]["generated_text"]

        try:
            return parser.parse(initial_raw)
        except Exception as e:
            error_message: str = str(e)
            retry_prompt_text: str = format_retry_prompt(error_message, initial_raw)
            retry_raw: str = pipe.invoke(retry_prompt_text)[0]["generated_text"]

            try:
                return parser.parse(retry_raw)
            except Exception as e:
                msg: str = (
                    f"CODE:7 | Failed to generate a valid output | {retry_raw} | {e}"
                )
                raise RuntimeError(msg)

    return RunnableLambda(invoke_with_retry)
