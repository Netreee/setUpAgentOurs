FROM ghcr.io/jetbrains-research/envbench-python:latest

# Repository: has2k1/plotnine
# Revision: 812a5ab0b591515c4f5b62c08b5e51f90ab4cae1

# Clone and checkout the specific revision
RUN git clone https://github.com/has2k1/plotnine.git /data/project && \
    cd /data/project && \
    git checkout 812a5ab0b591515c4f5b62c08b5e51f90ab4cae1

WORKDIR /data/project

# Copy install script
COPY SETUP_AND_INSTALL.sh /data/project/SETUP_AND_INSTALL.sh
RUN chmod +x /data/project/SETUP_AND_INSTALL.sh

# Run installation
RUN bash /data/project/SETUP_AND_INSTALL.sh
