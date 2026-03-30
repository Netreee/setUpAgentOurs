FROM ghcr.io/jetbrains-research/envbench-python:latest

# Repository: posit-dev/great-tables
# Revision: c4cbd943e9376c62872c3c402e64d168264e5623

# Clone and checkout the specific revision
RUN git clone https://github.com/posit-dev/great-tables.git /data/project && \
    cd /data/project && \
    git checkout c4cbd943e9376c62872c3c402e64d168264e5623

WORKDIR /data/project

# Copy install script
COPY SETUP_AND_INSTALL.sh /data/project/SETUP_AND_INSTALL.sh
RUN chmod +x /data/project/SETUP_AND_INSTALL.sh

# Run installation
RUN bash /data/project/SETUP_AND_INSTALL.sh
