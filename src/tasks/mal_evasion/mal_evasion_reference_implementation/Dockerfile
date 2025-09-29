FROM ubuntu:24.04

RUN apt-get update -y \
    && apt-get upgrade -y \
    && apt-get install -y \
    curl \
    python3 \
    python3-pip \
    python3-dev \
    python3-venv \
    jq \
    tmux \
    screen \
    wget \
    make \
    bash \
    git \
    file \
    grep \
    sed \
    gawk \
    coreutils \
    findutils \
    && apt-get clean

# Virtual environment setup
ENV VIRTUAL_ENV=/opt/venv
RUN python3 -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

RUN pip install --no-cache-dir flake8 numpy pandas matplotlib psutil seaborn beautifulsoup4 scipy scikit-learn scikit-image opencv-python scapy yara-python requests flask

# Here starts the stuff specific to this eval
# We don't strictly need pytest, but the model sometimes assumes we do, and it's harmless
RUN pip install --no-cache-dir pytest
RUN apt-get install -y yara
RUN mkdir -p /assets/
RUN chown -R ubuntu:ubuntu /assets

USER ubuntu
WORKDIR /home/ubuntu

CMD ["/bin/bash"]
