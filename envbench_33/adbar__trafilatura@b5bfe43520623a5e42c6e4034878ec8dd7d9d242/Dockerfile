FROM ghcr.io/jetbrains-research/envbench-python:latest

# Repository: adbar/trafilatura
# Revision: b5bfe43520623a5e42c6e4034878ec8dd7d9d242

# Clone and checkout the specific revision
RUN git clone https://github.com/adbar/trafilatura.git /data/project && \
    cd /data/project && \
    git checkout b5bfe43520623a5e42c6e4034878ec8dd7d9d242

WORKDIR /data/project

# Copy install script
COPY SETUP_AND_INSTALL.sh /data/project/SETUP_AND_INSTALL.sh
RUN chmod +x /data/project/SETUP_AND_INSTALL.sh

# Run installation
RUN bash /data/project/SETUP_AND_INSTALL.sh
