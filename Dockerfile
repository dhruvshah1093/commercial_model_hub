# Use Python 3.10 slim image as base
FROM python:3.10-slim
LABEL maintainer="dhruvshah1093"

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    python3-pip \
    sudo \
    curl && \
    apt-get clean

# Install GitHub CLI
RUN curl -fsSL https://cli.github.com/packages/githubcli-archive-keyring.gpg | dd of=/usr/share/keyrings/githubcli-archive-keyring.gpg && \
    chmod go+r /usr/share/keyrings/githubcli-archive-keyring.gpg && \
    echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/githubcli-archive-keyring.gpg] https://cli.github.com/packages stable main" | tee /etc/apt/sources.list.d/github-cli.list > /dev/null && \
    apt-get update && apt-get install -y gh

# Set environment variables
ENV PYTHONUNBUFFERED=1

# Default command to start Django NOTE: only for production 
# CMD ["/bin/sh", "-c", "/.devcontainer/scripts/start.sh"]
