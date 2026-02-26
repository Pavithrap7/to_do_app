FROM jenkins/jenkins:lts

# Switch to root to install packages
USER root

# Install Docker CLI + Python3 + pip + bash
RUN apt-get update && \
    apt-get install -y docker.io python3 python3-pip bash && \
    rm -rf /var/lib/apt/lists/*

# Switch back to jenkins user
USER jenkins
