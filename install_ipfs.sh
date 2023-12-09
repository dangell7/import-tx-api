#!/bin/bash

# Set the IPFS version to install
IPFS_VERSION="v0.24.0"

# Download the IPFS tarball
wget "https://dist.ipfs.io/go-ipfs/${IPFS_VERSION}/go-ipfs_${IPFS_VERSION}_linux-amd64.tar.gz"

# Extract the tarball
tar -xvzf "go-ipfs_${IPFS_VERSION}_linux-amd64.tar.gz"

# Move into the extracted directory
cd "go-ipfs" || exit

# Run the installation script
sudo bash install.sh

# Initialize the IPFS node
ipfs init

# Update the IPFS configuration to listen on all interfaces for the gateway
ipfs config Addresses.Gateway "/ip4/0.0.0.0/tcp/8080"

# Set the Garbage Collection configuration
ipfs config --json Datastore.GCPeriod '"1m"'
ipfs config --json Datastore.StorageGCWatermark 90

# Set the IPNS configuration
ipfs config --json Ipns.RecordLifetime '"1m"'
ipfs config --json Ipns.RepublishPeriod '"1m"'
ipfs config --json Ipns.ResolveCacheSize 10

# Create a systemd service file for IPFS
IPFS_SERVICE_FILE="/etc/systemd/system/ipfs.service"
echo "[Unit]
Description=IPFS Daemon
After=network.target

[Service]
User=$USER
ExecStart=/usr/local/bin/ipfs daemon
Restart=on-failure

[Install]
WantedBy=multi-user.target" | sudo tee "$IPFS_SERVICE_FILE"

# Enable and start the IPFS service
sudo systemctl enable ipfs
sudo systemctl start ipfs

# Clean up downloaded files
cd ..
rm -rf "go-ipfs_${IPFS_VERSION}_linux-amd64.tar.gz" "go-ipfs"

# Open necessary ports for IPFS on UFW
sudo ufw allow 4001/tcp comment 'IPFS Swarm'
# sudo ufw allow 5001/tcp comment 'IPFS API'
sudo ufw allow 8080/tcp comment 'IPFS Gateway'
sudo ufw allow 9000/tcp comment 'IPNS Xumm API'

# Reload UFW to apply the changes
sudo ufw reload

# Check the status of the IPFS service
echo "IPFS service status:"
sudo systemctl status ipfs --no-pager

# Check UFW status to confirm ports are open
echo "UFW status:"
sudo ufw status numbered