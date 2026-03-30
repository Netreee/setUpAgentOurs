FROM ghcr.io/jetbrains-research/envbench-python:latest

# Repository: vacanza/python-holidays
# Revision: 472e89d889cf3a5c5301d54bc642f6c149f55ee5

# Clone and checkout the specific revision
RUN git clone https://github.com/vacanza/python-holidays.git /data/project && \
    cd /data/project && \
    git checkout 472e89d889cf3a5c5301d54bc642f6c149f55ee5

WORKDIR /data/project

# Copy install script
COPY SETUP_AND_INSTALL.sh /data/project/SETUP_AND_INSTALL.sh
RUN chmod +x /data/project/SETUP_AND_INSTALL.sh

# Run installation
RUN bash /data/project/SETUP_AND_INSTALL.sh
