#!/bin/bash
# ==============================================================================
# SentinelVultr - Automated Deployment Script for Vultr Cloud Compute VM
# Target OS: Ubuntu 22.04 LTS / Ubuntu 24.04 LTS
# ==============================================================================

set -e

echo "======================================================================"
echo "   Deploying SentinelVultr on Vultr Cloud Compute (Blast Radius Zero) "
echo "======================================================================"

# Step 1: Update OS Packages
echo "[1/6] Updating system packages..."
apt-get update && apt-get upgrade -y
apt-get install -y curl git ufw jq ca-certificates gnupg

# Step 2: Install Docker Engine
echo "[2/6] Installing Docker & Docker Compose..."
if ! command -v docker &> /dev/null; then
    install -m 0755 -d /etc/apt/keyrings
    curl -fsSL https://download.docker.com/linux/ubuntu/gpg | gpg --dearmor -o /etc/apt/keyrings/docker.gpg
    chmod a+r /etc/apt/keyrings/docker.gpg

    echo \
      "deb [arch="$(dpkg --print-architecture)" signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu \
      "$(. /etc/os-release && echo "$VERSION_CODENAME")" stable" | \
      tee /etc/apt/sources.list.d/docker.list > /dev/null

    apt-get update
    apt-get install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
    systemctl enable docker
    systemctl start docker
    echo "Docker installed successfully."
else
    echo "Docker already installed."
fi

# Step 3: Configure UFW Firewall
echo "[3/6] Configuring Host Firewall (UFW)..."
ufw allow 22/tcp
ufw allow 80/tcp
ufw allow 443/tcp
ufw allow 3000/tcp  # Web App Frontend
ufw allow 8000/tcp  # FastAPI Control Plane
ufw --force enable

# Step 4: Pull Base Sandbox Images
echo "[4/6] Pre-pulling isolated sandbox runtimes..."
docker pull python:3.11-slim

# Step 5: Configure Environment Variables
echo "[5/6] Checking environment..."
if [ ! -f .env ]; then
    echo "Creating .env template..."
    cat <<EOT >> .env
VULTR_API_KEY=""
VULTR_INFERENCE_BASE_URL="https://api.vultrinference.com/v1"
VULTR_MODEL="meta-llama/llama-3.3-70b-instruct"
MAX_MEMORY_MB=512
MAX_CPU_QUOTA=1.0
BLOCK_NETWORK_FOR_CODE=true
EOT
    echo "Please set your VULTR_API_KEY in .env if available (or use the built-in emulator)."
fi

# Step 6: Launch with Docker Compose
echo "[6/6] Launching SentinelVultr Stack..."
docker compose -f deploy/docker-compose.yml up -d --build

echo "======================================================================"
echo "   DEPLOYMENT COMPLETE! "
echo "   Web Application URL: http://$(curl -s https://api.ipify.org):3000"
echo "   Backend API Docs:    http://$(curl -s https://api.ipify.org):8000/docs"
echo "======================================================================"

