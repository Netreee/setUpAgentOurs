FROM ghcr.io/jetbrains-research/envbench-python:latest

# Repository: alteryx/featuretools
# Revision: 8c99ff7d62d723e90d406ac56bae22aad82e6a47

# Clone and checkout the specific revision
RUN git clone https://github.com/alteryx/featuretools.git /data/project && \
    cd /data/project && \
    git checkout 8c99ff7d62d723e90d406ac56bae22aad82e6a47

WORKDIR /data/project

# Copy install script
COPY SETUP_AND_INSTALL.sh /data/project/SETUP_AND_INSTALL.sh
RUN chmod +x /data/project/SETUP_AND_INSTALL.sh

# Run installation
RUN bash /data/project/SETUP_AND_INSTALL.sh
