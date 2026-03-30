FROM ghcr.io/jetbrains-research/envbench-python:latest

# Repository: tmux-python/tmuxp
# Revision: 3e0fec3596cc557456af4f51e66a72aebbfe7ff8

# Clone and checkout the specific revision
RUN git clone https://github.com/tmux-python/tmuxp.git /data/project && \
    cd /data/project && \
    git checkout 3e0fec3596cc557456af4f51e66a72aebbfe7ff8

WORKDIR /data/project

# Copy install script
COPY SETUP_AND_INSTALL.sh /data/project/SETUP_AND_INSTALL.sh
RUN chmod +x /data/project/SETUP_AND_INSTALL.sh

# Run installation
RUN bash /data/project/SETUP_AND_INSTALL.sh
