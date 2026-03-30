FROM ghcr.io/jetbrains-research/envbench-python:latest

# Repository: lmcinnes/umap
# Revision: b45cece876513b3f95bd2dc7cb400240b1edab2a

# Clone and checkout the specific revision
RUN git clone https://github.com/lmcinnes/umap.git /data/project && \
    cd /data/project && \
    git checkout b45cece876513b3f95bd2dc7cb400240b1edab2a

WORKDIR /data/project

# Copy install script
COPY SETUP_AND_INSTALL.sh /data/project/SETUP_AND_INSTALL.sh
RUN chmod +x /data/project/SETUP_AND_INSTALL.sh

# Run installation
RUN bash /data/project/SETUP_AND_INSTALL.sh
