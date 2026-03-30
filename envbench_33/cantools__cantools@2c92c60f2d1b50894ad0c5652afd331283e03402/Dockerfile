FROM ghcr.io/jetbrains-research/envbench-python:latest

# Repository: cantools/cantools
# Revision: 2c92c60f2d1b50894ad0c5652afd331283e03402

# Clone and checkout the specific revision
RUN git clone https://github.com/cantools/cantools.git /data/project && \
    cd /data/project && \
    git checkout 2c92c60f2d1b50894ad0c5652afd331283e03402

WORKDIR /data/project

# Copy install script
COPY SETUP_AND_INSTALL.sh /data/project/SETUP_AND_INSTALL.sh
RUN chmod +x /data/project/SETUP_AND_INSTALL.sh

# Run installation
RUN bash /data/project/SETUP_AND_INSTALL.sh
