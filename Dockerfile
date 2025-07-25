# author --> Skye Lane Goetz

# mamaba
FROM mambaorg/micromamba:1.6.2

WORKDIR /TABLE_CONFIG_AGENT

COPY . .

RUN micromamba env create -f /tmp/environment.yml -n table-confog-agent && micromamba clean --all --yes
ENV PATH=/opt/conda/envs/myenv/bin:$PATH



