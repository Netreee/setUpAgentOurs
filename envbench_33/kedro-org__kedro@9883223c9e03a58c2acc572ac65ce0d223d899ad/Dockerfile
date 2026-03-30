FROM ghcr.io/jetbrains-research/envbench-python:latest

# Repository: kedro-org/kedro
# Revision: 9883223c9e03a58c2acc572ac65ce0d223d899ad

# Clone and checkout the specific revision
RUN git clone https://github.com/kedro-org/kedro.git /data/project && \
    cd /data/project && \
    git checkout 9883223c9e03a58c2acc572ac65ce0d223d899ad

WORKDIR /data/project

# Copy install script
COPY SETUP_AND_INSTALL.sh /data/project/SETUP_AND_INSTALL.sh
RUN chmod +x /data/project/SETUP_AND_INSTALL.sh

# Run installation
RUN bash /data/project/SETUP_AND_INSTALL.sh
