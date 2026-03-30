FROM ghcr.io/jetbrains-research/envbench-python:latest

# Repository: platformio/platformio-core
# Revision: 7cf8d1d6961761eab681d49eea7fbafae0889186

# Clone and checkout the specific revision
RUN git clone https://github.com/platformio/platformio-core.git /data/project && \
    cd /data/project && \
    git checkout 7cf8d1d6961761eab681d49eea7fbafae0889186

WORKDIR /data/project

# Copy install script
COPY SETUP_AND_INSTALL.sh /data/project/SETUP_AND_INSTALL.sh
RUN chmod +x /data/project/SETUP_AND_INSTALL.sh

# Run installation
RUN bash /data/project/SETUP_AND_INSTALL.sh
