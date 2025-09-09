# TableConfigAgent Configuration

## Version 0.1.0

### By Skye Lane Goetz

## Database Configuration

Usage (Example)
```yaml
from_transformers: Qwen/Qwen2.5-Coder-14B-Instruct
using_chroma_db: resources/dev/chroma_db/AUG_11_QWEN_14B_INSTRUCT
offload_folder: /dev/shm/
fewshot_count: 6
seed: 87
```

Options
|Key|Description|Default|
|-|-|-|
|from_transformers|A Hugging Face transformer to use for the Langchain Agent|NA|
|using_chroma_db|A path to the ChromaDB you want to make from examples or use again if precomputed|NA|
|offload_folder|A path to an Offload Folder for the Pipeline|NA|
|fewshot_count|The number of fewshot examples from the ChromaDB to use for every relevant prompt|4|
|seed|A deterministic seed to use for neural net generation|87|

## Return To Root

[Click Me](../README.md)