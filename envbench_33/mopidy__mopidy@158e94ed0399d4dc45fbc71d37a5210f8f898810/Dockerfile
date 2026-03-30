FROM ghcr.io/jetbrains-research/envbench-python:latest

# Repository: mopidy/mopidy
# Revision: 158e94ed0399d4dc45fbc71d37a5210f8f898810

# Clone and checkout the specific revision
RUN git clone https://github.com/mopidy/mopidy.git /data/project && \
    cd /data/project && \
    git checkout 158e94ed0399d4dc45fbc71d37a5210f8f898810

WORKDIR /data/project

# Copy install script
COPY SETUP_AND_INSTALL.sh /data/project/SETUP_AND_INSTALL.sh
RUN chmod +x /data/project/SETUP_AND_INSTALL.sh

# Run installation
RUN bash /data/project/SETUP_AND_INSTALL.sh
