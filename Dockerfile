# author --> Skye Lane Goetz

# mamba
FROM mambaorg/micromamba:1.6.2

WORKDIR /TABLE_CONFIG_AGENT
EXPOSE 8080

COPY . .

RUN micromamba env create -f /tmp/environment.yaml -n table-config-agent && micromamba clean --all --yes
ENV PATH=/opt/conda/envs/myenv/bin:$PATH

# typer cli
ENTRYPOINT ["python3", "-m", "src/table_config_agent/ui/cli.py"]
CMD ["--help"]