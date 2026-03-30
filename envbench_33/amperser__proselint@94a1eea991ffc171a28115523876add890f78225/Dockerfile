FROM ghcr.io/jetbrains-research/envbench-python:latest

# Repository: amperser/proselint
# Revision: 94a1eea991ffc171a28115523876add890f78225

# Clone and checkout the specific revision
RUN git clone https://github.com/amperser/proselint.git /data/project && \
    cd /data/project && \
    git checkout 94a1eea991ffc171a28115523876add890f78225

WORKDIR /data/project

# Copy install script
COPY SETUP_AND_INSTALL.sh /data/project/SETUP_AND_INSTALL.sh
RUN chmod +x /data/project/SETUP_AND_INSTALL.sh

# Run installation
RUN bash /data/project/SETUP_AND_INSTALL.sh
