FROM ghcr.io/jetbrains-research/envbench-python:latest

# Repository: piskvorky/smart_open
# Revision: 5a826134eb23c86087d06db3b78b25484e7e2e6d

# Clone and checkout the specific revision
RUN git clone https://github.com/piskvorky/smart_open.git /data/project && \
    cd /data/project && \
    git checkout 5a826134eb23c86087d06db3b78b25484e7e2e6d

WORKDIR /data/project

# Copy install script
COPY SETUP_AND_INSTALL.sh /data/project/SETUP_AND_INSTALL.sh
RUN chmod +x /data/project/SETUP_AND_INSTALL.sh

# Run installation
RUN bash /data/project/SETUP_AND_INSTALL.sh
