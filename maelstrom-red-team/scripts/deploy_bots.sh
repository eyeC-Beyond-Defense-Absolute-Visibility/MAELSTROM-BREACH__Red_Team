#!/bin/bash

# --- Configuration ---
BOT_CONFIG="../c2-controller/config.json"
REMOTE_DIR="/tmp/maelstrom"
USER="user" # Change this to your Ubuntu username

# Extract IPs from JSON using grep/sed (to avoid requiring 'jq' on Kali)
IPS=$(grep -oP '(?<="ip": ")[^"]*' $BOT_CONFIG)

echo "[*] Starting Maelstrom Deployment..."

for IP in $IPS; do
    echo "----------------------------------------------------"
    echo "[+] Deploying to: $IP"

    # 1. Create remote directory
    ssh $USER@$IP "mkdir -p $REMOTE_DIR/modules"

    # 2. Copy the agent and modules
    # We use -r to copy the entire bot-scripts folder content
    scp -r ../bot-scripts/* $USER@$IP:$REMOTE_DIR/

    # 3. Install dependencies
    # This ensures Scapy and Requests are present on the target
    echo "[*] Installing dependencies on $IP..."
    ssh $USER@$IP "sudo apt-get update -qq && sudo apt-get install -y python3-pip -qq"
    ssh $USER@$IP "pip3 install -r $REMOTE_DIR/requirements.txt --quiet"

    echo "[V] Deployment complete for $IP"
done

echo "----------------------------------------------------"
echo "[!] All nodes are synchronized and ready for orders."