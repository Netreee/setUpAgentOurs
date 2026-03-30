FROM ghcr.io/jetbrains-research/envbench-python:latest

# Repository: pypa/pip
# Revision: 67e2a5698706751161d8af3dad1dbb8e62bc8cbb

# Clone and checkout the specific revision
RUN git clone https://github.com/pypa/pip.git /data/project && \
    cd /data/project && \
    git checkout 67e2a5698706751161d8af3dad1dbb8e62bc8cbb

WORKDIR /data/project

# Copy install script
COPY SETUP_AND_INSTALL.sh /data/project/SETUP_AND_INSTALL.sh
RUN chmod +x /data/project/SETUP_AND_INSTALL.sh

# Run installation
RUN bash /data/project/SETUP_AND_INSTALL.sh
