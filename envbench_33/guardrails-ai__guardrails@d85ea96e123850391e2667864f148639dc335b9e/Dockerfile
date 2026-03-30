FROM ghcr.io/jetbrains-research/envbench-python:latest

# Repository: guardrails-ai/guardrails
# Revision: d85ea96e123850391e2667864f148639dc335b9e

# Clone and checkout the specific revision
RUN git clone https://github.com/guardrails-ai/guardrails.git /data/project && \
    cd /data/project && \
    git checkout d85ea96e123850391e2667864f148639dc335b9e

WORKDIR /data/project

# Copy install script
COPY SETUP_AND_INSTALL.sh /data/project/SETUP_AND_INSTALL.sh
RUN chmod +x /data/project/SETUP_AND_INSTALL.sh

# Run installation
RUN bash /data/project/SETUP_AND_INSTALL.sh
