FROM nvidia/cuda:11.8.0-cudnn8-devel-ubuntu22.04
FROM python:3.8

ARG DEBIAN_FRONTEND=noninteractive

ENV PYTHONUNBUFFERED=1

RUN apt-get update && apt-get install --no-install-recommends -y \
  build-essential \
  git \
  ffmpeg \
  curl \
  vim \
  python3-setuptools \  
  && apt-get clean && rm -rf /var/lib/apt/lists/*

# Disable the Git warning
ENV GIT_REV_PARSE_IS_INSIDE_WORK_TREE=0

# Disable BuildKit
ENV DOCKER_BUILDKIT=0

# Install Rust using the Rustup script
RUN curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y

# Add Rust to the PATH
ENV PATH=$PATH:/root/.cargo/bin

# Verify Rust installation
RUN rustc --version

WORKDIR /app

COPY ./requirements.txt /app/requirements.txt

RUN pip3 install --no-cache-dir --upgrade -r /app/requirements.txt

WORKDIR /app
COPY ./app /app
RUN pip install --no-cache-dir --upgrade transformers

# Start the FastAPI app
CMD ["uvicorn", "fast_app:app", "--host", "0.0.0.0", "--port", "8080"]

