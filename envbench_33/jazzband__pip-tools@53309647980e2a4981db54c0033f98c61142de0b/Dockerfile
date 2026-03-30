FROM ghcr.io/jetbrains-research/envbench-python:latest

# Repository: jazzband/pip-tools
# Revision: 53309647980e2a4981db54c0033f98c61142de0b

# Clone and checkout the specific revision
RUN git clone https://github.com/jazzband/pip-tools.git /data/project && \
    cd /data/project && \
    git checkout 53309647980e2a4981db54c0033f98c61142de0b

WORKDIR /data/project

# Copy install script
COPY SETUP_AND_INSTALL.sh /data/project/SETUP_AND_INSTALL.sh
RUN chmod +x /data/project/SETUP_AND_INSTALL.sh

# Run installation
RUN bash /data/project/SETUP_AND_INSTALL.sh
