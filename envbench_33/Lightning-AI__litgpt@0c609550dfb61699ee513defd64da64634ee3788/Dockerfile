FROM ghcr.io/jetbrains-research/envbench-python:latest

# Repository: Lightning-AI/litgpt
# Revision: 0c609550dfb61699ee513defd64da64634ee3788

# Clone and checkout the specific revision
RUN git clone https://github.com/Lightning-AI/litgpt.git /data/project && \
    cd /data/project && \
    git checkout 0c609550dfb61699ee513defd64da64634ee3788

WORKDIR /data/project

# Copy install script
COPY SETUP_AND_INSTALL.sh /data/project/SETUP_AND_INSTALL.sh
RUN chmod +x /data/project/SETUP_AND_INSTALL.sh

# Run installation
RUN bash /data/project/SETUP_AND_INSTALL.sh
