# Use Python 3.10 slim image as base
FROM python:3.10-slim
LABEL maintainer="dhruvshah1093"

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    python3-pip \
    sudo && \
    apt-get clean

# Install GitHub CLI
RUN apt-get update && apt-get install -y \
    curl && \
    curl -fsSL https://cli.github.com/packages/githubcli-archive-keyring.gpg | dd of=/usr/share/keyrings/githubcli-archive-keyring.gpg && \
    chmod go+r /usr/share/keyrings/githubcli-archive-keyring.gpg && \
    echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/githubcli-archive-keyring.gpg] https://cli.github.com/packages stable main" | tee /etc/apt/sources.list.d/github-cli.list > /dev/null && \
    apt-get update && apt-get install -y gh

# # Set working directory
# ARG REPO_NAME=default-repo
# WORKDIR /app

# # Note: You can create a virtual environment and activate it here : this is to avoid any conflicts between the system packages and packges required for the project.
# # Install Python dependencies
# COPY requirements.txt .
# RUN pip install --no-cache-dir -r requirements.txt

# # Copy the rest of the application code
# COPY . .

# # Set environment variables
# ENV PYTHONUNBUFFERED=1

EXPOSE 8000

# RUN cd scripts && chmod +x start.sh

# Default command to keep container running
CMD ["tail", "-f", "/dev/null"]
