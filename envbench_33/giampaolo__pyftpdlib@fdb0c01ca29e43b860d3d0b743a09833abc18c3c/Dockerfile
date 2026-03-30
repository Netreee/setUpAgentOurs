FROM ghcr.io/jetbrains-research/envbench-python:latest

# Repository: giampaolo/pyftpdlib
# Revision: fdb0c01ca29e43b860d3d0b743a09833abc18c3c

# Clone and checkout the specific revision
RUN git clone https://github.com/giampaolo/pyftpdlib.git /data/project && \
    cd /data/project && \
    git checkout fdb0c01ca29e43b860d3d0b743a09833abc18c3c

WORKDIR /data/project

# Copy install script
COPY SETUP_AND_INSTALL.sh /data/project/SETUP_AND_INSTALL.sh
RUN chmod +x /data/project/SETUP_AND_INSTALL.sh

# Run installation
RUN bash /data/project/SETUP_AND_INSTALL.sh
