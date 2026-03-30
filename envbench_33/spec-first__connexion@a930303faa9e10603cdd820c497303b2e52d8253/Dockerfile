FROM ghcr.io/jetbrains-research/envbench-python:latest

# Repository: spec-first/connexion
# Revision: a930303faa9e10603cdd820c497303b2e52d8253

# Clone and checkout the specific revision
RUN git clone https://github.com/spec-first/connexion.git /data/project && \
    cd /data/project && \
    git checkout a930303faa9e10603cdd820c497303b2e52d8253

WORKDIR /data/project

# Copy install script
COPY SETUP_AND_INSTALL.sh /data/project/SETUP_AND_INSTALL.sh
RUN chmod +x /data/project/SETUP_AND_INSTALL.sh

# Run installation
RUN bash /data/project/SETUP_AND_INSTALL.sh
