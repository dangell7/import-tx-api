#!/bin/bash

# Variables
DOMAIN="yourdomain.com"
EMAIL="youremail@example.com" # Replace with your email address for Let's Encrypt notifications

# Install Nginx
sudo apt update
sudo apt install -y nginx

# Create Nginx server block configuration
NGINX_CONF="/etc/nginx/sites-available/ipfs.conf"
echo "server {
    listen 80;
    server_name $DOMAIN;

    location / {
        proxy_pass http://localhost:8080;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
    }
}" | sudo tee "$NGINX_CONF"

# Enable the new Nginx server block
sudo ln -s "$NGINX_CONF" /etc/nginx/sites-enabled/

# Test Nginx configuration and reload if successful
sudo nginx -t && sudo systemctl reload nginx

# Install Certbot and the Nginx plugin
sudo apt install -y certbot python3-certbot-nginx

# Obtain an SSL certificate and configure Nginx to use it
sudo certbot --nginx -d "$DOMAIN" --non-interactive --agree-tos --email "$EMAIL"

# Reload Nginx to apply SSL settings
sudo systemctl reload nginx

echo "Nginx reverse proxy setup complete. IPFS gateway is now accessible via https://$DOMAIN"