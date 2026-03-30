FROM ghcr.io/jetbrains-research/envbench-python:latest

# Repository: embeddings-benchmark/mteb
# Revision: e169fb30e4f2cb01cdd1fa0667a325a6a73b5c01

# Clone and checkout the specific revision
RUN git clone https://github.com/embeddings-benchmark/mteb.git /data/project && \
    cd /data/project && \
    git checkout e169fb30e4f2cb01cdd1fa0667a325a6a73b5c01

WORKDIR /data/project

# Copy install script
COPY SETUP_AND_INSTALL.sh /data/project/SETUP_AND_INSTALL.sh
RUN chmod +x /data/project/SETUP_AND_INSTALL.sh

# Run installation
RUN bash /data/project/SETUP_AND_INSTALL.sh
