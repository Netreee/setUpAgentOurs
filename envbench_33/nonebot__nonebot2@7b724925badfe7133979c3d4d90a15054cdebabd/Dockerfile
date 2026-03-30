FROM ghcr.io/jetbrains-research/envbench-python:latest

# Repository: nonebot/nonebot2
# Revision: 7b724925badfe7133979c3d4d90a15054cdebabd

# Clone and checkout the specific revision
RUN git clone https://github.com/nonebot/nonebot2.git /data/project && \
    cd /data/project && \
    git checkout 7b724925badfe7133979c3d4d90a15054cdebabd

WORKDIR /data/project

# Copy install script
COPY SETUP_AND_INSTALL.sh /data/project/SETUP_AND_INSTALL.sh
RUN chmod +x /data/project/SETUP_AND_INSTALL.sh

# Run installation
RUN bash /data/project/SETUP_AND_INSTALL.sh
