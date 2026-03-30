FROM ghcr.io/jetbrains-research/envbench-python:latest

# Repository: pypa/twine
# Revision: 6fbf880ee60915cf1666348c4bdd78a10415f2ac

# Clone and checkout the specific revision
RUN git clone https://github.com/pypa/twine.git /data/project && \
    cd /data/project && \
    git checkout 6fbf880ee60915cf1666348c4bdd78a10415f2ac

WORKDIR /data/project

# Copy install script
COPY SETUP_AND_INSTALL.sh /data/project/SETUP_AND_INSTALL.sh
RUN chmod +x /data/project/SETUP_AND_INSTALL.sh

# Run installation
RUN bash /data/project/SETUP_AND_INSTALL.sh
