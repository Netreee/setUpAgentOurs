FROM ghcr.io/jetbrains-research/envbench-python:latest

# Repository: getsentry/sentry-python
# Revision: ec7172e15311b88695827a76ca7fa83fba2efff4

# Clone and checkout the specific revision
RUN git clone https://github.com/getsentry/sentry-python.git /data/project && \
    cd /data/project && \
    git checkout ec7172e15311b88695827a76ca7fa83fba2efff4

WORKDIR /data/project

# Copy install script
COPY SETUP_AND_INSTALL.sh /data/project/SETUP_AND_INSTALL.sh
RUN chmod +x /data/project/SETUP_AND_INSTALL.sh

# Run installation
RUN bash /data/project/SETUP_AND_INSTALL.sh
