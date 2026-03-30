FROM ghcr.io/jetbrains-research/envbench-python:latest

# Repository: castagnait/plugin.video.netflix
# Revision: e87aa8559e9b0d38699a5383e09381ee7756783b

# Clone and checkout the specific revision
RUN git clone https://github.com/castagnait/plugin.video.netflix.git /data/project && \
    cd /data/project && \
    git checkout e87aa8559e9b0d38699a5383e09381ee7756783b

WORKDIR /data/project

# Copy install script
COPY SETUP_AND_INSTALL.sh /data/project/SETUP_AND_INSTALL.sh
RUN chmod +x /data/project/SETUP_AND_INSTALL.sh

# Run installation
RUN bash /data/project/SETUP_AND_INSTALL.sh
