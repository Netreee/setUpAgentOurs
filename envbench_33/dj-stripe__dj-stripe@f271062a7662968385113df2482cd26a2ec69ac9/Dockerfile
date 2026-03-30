FROM ghcr.io/jetbrains-research/envbench-python:latest

# Repository: dj-stripe/dj-stripe
# Revision: f271062a7662968385113df2482cd26a2ec69ac9

# Clone and checkout the specific revision
RUN git clone https://github.com/dj-stripe/dj-stripe.git /data/project && \
    cd /data/project && \
    git checkout f271062a7662968385113df2482cd26a2ec69ac9

WORKDIR /data/project

# Copy install script
COPY SETUP_AND_INSTALL.sh /data/project/SETUP_AND_INSTALL.sh
RUN chmod +x /data/project/SETUP_AND_INSTALL.sh

# Run installation
RUN bash /data/project/SETUP_AND_INSTALL.sh
