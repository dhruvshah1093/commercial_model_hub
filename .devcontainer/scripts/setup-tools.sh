#!/bin/bash
set -e
echo " Installing Project requirments"
pip install --upgrade pip && pip install -r requirements.txt

echo "🔧 Installing AWS CLI..."
curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
unzip -q awscliv2.zip
sudo ./aws/install
rm -rf aws awscliv2.zip

echo "🚜 Installing Minikube..."
curl -Lo minikube https://storage.googleapis.com/minikube/releases/latest/minikube-linux-amd64
chmod +x minikube
sudo mv minikube /usr/local/bin/

echo "✅ Tools installed!"

echo "Start development script"

# echo "🚀 Starting Minikube with 4GB RAM..."
# minikube start --memory=4096 --driver=docker --force
