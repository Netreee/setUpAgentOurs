FROM ghcr.io/jetbrains-research/envbench-python:latest

# Repository: ethereum/py-evm
# Revision: d8df507e42c885ddeca2b64bbb8f10705f075d3e

# Clone and checkout the specific revision
RUN git clone https://github.com/ethereum/py-evm.git /data/project && \
    cd /data/project && \
    git checkout d8df507e42c885ddeca2b64bbb8f10705f075d3e

WORKDIR /data/project

# Copy install script
COPY SETUP_AND_INSTALL.sh /data/project/SETUP_AND_INSTALL.sh
RUN chmod +x /data/project/SETUP_AND_INSTALL.sh

# Run installation
RUN bash /data/project/SETUP_AND_INSTALL.sh
