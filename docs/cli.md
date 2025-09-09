# TableConfigAgent CLI

## Version 0.1.0

### By Skye Lane Goetz

## chroma-build
Builds the chroma_db for agent from examples in src.table_config_agent.chroma_db and finetunes transformers with chroma_db data

Usage
```bash
TCAGENT chroma-build --help
```

Options
|Option|Description|Default|
|-|-|-|
|-d|path specifiying the directory where you want to save the chroma_db build|resources/chroma_db|
|-m|path to your ModelConfig (model.yaml)|NA|
|-b|FLAG: creates a timestamped xz compressed backup of the previous chroma_db build|False|

## invoke-agent
Invokes the TableConfigAgent turning a natural language input into a Tablassert TableConfig

Usage
```bash
TCAGENT invoke-agent --help
```
Options
|Option|Description|Default|
|-|-|-|
|-i|freetext input that the TableConfigAgent attempts to generate a TableConfig from|NA|
|-n|your name, its required to build a valid TableConfig|NA|
|-o|the organization you represent, its required to build a valid TableConfig|NA|
|-p|path specifiying where you want to save your TableConfig.yaml|resources/config/table/table_config.yaml|
|-m|path to your ModelConfig (model.yaml)|NA|

## Return To Root

[Click Me](../README.md)