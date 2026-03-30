FROM ghcr.io/jetbrains-research/envbench-python:latest

# Repository: tortoise/tortoise-orm
# Revision: bc18384bdb490cc14e96d27a18956fe1b122829d

# Clone and checkout the specific revision
RUN git clone https://github.com/tortoise/tortoise-orm.git /data/project && \
    cd /data/project && \
    git checkout bc18384bdb490cc14e96d27a18956fe1b122829d

WORKDIR /data/project

# Copy install script
COPY SETUP_AND_INSTALL.sh /data/project/SETUP_AND_INSTALL.sh
RUN chmod +x /data/project/SETUP_AND_INSTALL.sh

# Run installation
RUN bash /data/project/SETUP_AND_INSTALL.sh
