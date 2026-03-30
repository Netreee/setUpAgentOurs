FROM ghcr.io/jetbrains-research/envbench-python:latest

# Repository: hips/autograd
# Revision: 9c756149ec3020286b21434023064226c9174b1a

# Clone and checkout the specific revision
RUN git clone https://github.com/hips/autograd.git /data/project && \
    cd /data/project && \
    git checkout 9c756149ec3020286b21434023064226c9174b1a

WORKDIR /data/project

# Copy install script
COPY SETUP_AND_INSTALL.sh /data/project/SETUP_AND_INSTALL.sh
RUN chmod +x /data/project/SETUP_AND_INSTALL.sh

# Run installation
RUN bash /data/project/SETUP_AND_INSTALL.sh
