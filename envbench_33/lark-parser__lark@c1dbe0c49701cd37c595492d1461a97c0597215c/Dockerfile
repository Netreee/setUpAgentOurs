FROM ghcr.io/jetbrains-research/envbench-python:latest

# Repository: lark-parser/lark
# Revision: c1dbe0c49701cd37c595492d1461a97c0597215c

# Clone and checkout the specific revision
RUN git clone https://github.com/lark-parser/lark.git /data/project && \
    cd /data/project && \
    git checkout c1dbe0c49701cd37c595492d1461a97c0597215c

WORKDIR /data/project

# Copy install script
COPY SETUP_AND_INSTALL.sh /data/project/SETUP_AND_INSTALL.sh
RUN chmod +x /data/project/SETUP_AND_INSTALL.sh

# Run installation
RUN bash /data/project/SETUP_AND_INSTALL.sh
