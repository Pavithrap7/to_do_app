# Start from Jenkins LTS image
FROM jenkins/jenkins:lts

# Switch to root to install packages
USER root

# Install Docker CLI and Python
RUN apt-get update && \
    apt-get install -y docker.io python3 python3-pip bash && \
    rm -rf /var/lib/apt/lists/*

# Set working directory for your app
WORKDIR /app

# Copy your app code into the container
COPY . /app

# Upgrade pip and install app dependencies
RUN pip3 install --upgrade pip
RUN pip3 install -r requirements.txt

# Optional: install dev tools for CI (lint, test, security)
RUN pip3 install flake8 pytest safety

# Expose ports: Jenkins + your app
EXPOSE 8080 5000

# Switch back to jenkins user
USER jenkins

# Start command: Jenkins runs by default, your app can be started from pipeline
# If you want, you can also start app directly in background (optional)
