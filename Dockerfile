FROM ubuntu:18.04

# Avoid tzdata prompts
ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get install -y \
    build-essential \
    bc \
    bison \
    flex \
    libssl-dev \
    libncurses5-dev \
    python2.7 \
    python-minimal \
    git \
    rsync \
    u-boot-tools \
    curl \
    zip \
    cpio \
    ca-certificates \
    libelf-dev \
    lzop \
    && rm -rf /var/lib/apt/lists/*

# Set python to python2.7 for legacy build scripts
RUN ln -sf /usr/bin/python2.7 /usr/bin/python

WORKDIR /workspace
