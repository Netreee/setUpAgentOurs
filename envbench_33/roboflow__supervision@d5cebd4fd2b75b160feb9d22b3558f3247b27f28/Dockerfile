FROM ghcr.io/jetbrains-research/envbench-python:latest

# Repository: roboflow/supervision
# Revision: d5cebd4fd2b75b160feb9d22b3558f3247b27f28

# Clone and checkout the specific revision
RUN git clone https://github.com/roboflow/supervision.git /data/project && \
    cd /data/project && \
    git checkout d5cebd4fd2b75b160feb9d22b3558f3247b27f28

WORKDIR /data/project

# Copy install script
COPY SETUP_AND_INSTALL.sh /data/project/SETUP_AND_INSTALL.sh
RUN chmod +x /data/project/SETUP_AND_INSTALL.sh

# Run installation
RUN bash /data/project/SETUP_AND_INSTALL.sh
