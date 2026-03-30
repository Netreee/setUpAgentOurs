FROM ghcr.io/jetbrains-research/envbench-python:latest

# Repository: mampfes/hacs_waste_collection_schedule
# Revision: a107f0e393b8f77b0da7971e530d0996344c6248

# Clone and checkout the specific revision
RUN git clone https://github.com/mampfes/hacs_waste_collection_schedule.git /data/project && \
    cd /data/project && \
    git checkout a107f0e393b8f77b0da7971e530d0996344c6248

WORKDIR /data/project

# Copy install script
COPY SETUP_AND_INSTALL.sh /data/project/SETUP_AND_INSTALL.sh
RUN chmod +x /data/project/SETUP_AND_INSTALL.sh

# Run installation
RUN bash /data/project/SETUP_AND_INSTALL.sh
