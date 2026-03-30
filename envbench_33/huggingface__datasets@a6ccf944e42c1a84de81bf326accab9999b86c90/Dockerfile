FROM ghcr.io/jetbrains-research/envbench-python:latest

# Repository: huggingface/datasets
# Revision: a6ccf944e42c1a84de81bf326accab9999b86c90

# Clone and checkout the specific revision
RUN git clone https://github.com/huggingface/datasets.git /data/project && \
    cd /data/project && \
    git checkout a6ccf944e42c1a84de81bf326accab9999b86c90

WORKDIR /data/project

# Copy install script
COPY SETUP_AND_INSTALL.sh /data/project/SETUP_AND_INSTALL.sh
RUN chmod +x /data/project/SETUP_AND_INSTALL.sh

# Run installation
RUN bash /data/project/SETUP_AND_INSTALL.sh
