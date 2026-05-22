#!/bin/bash
# ==============================================================================
# Setup Script for Apache, MariaDB (MySQL), and PHP on Raspberry Pi 4
# ==============================================================================
# WARNING: Run this with extreme care, it installs system packages.
# Usage: sudo bash setup.sh

echo "Updating package lists..."
apt update

echo "Installing Apache, MariaDB, PHP, and required extensions..."
# We use mariadb-server which is the default, fully compatible MySQL replacement on RPi.
apt install -y mariadb-server apache2 php libapache2-mod-php php-mysql php-curl python3-pymysql python3-requests curl

echo "Enabling and starting services..."
systemctl enable mariadb
systemctl start mariadb
systemctl enable apache2
systemctl start apache2

echo "Initializing Database..."
# Run the schema script to setup database, tables, and user
mariadb < schema.sql

echo "Deploying the PHP Web Dashboard..."
# Create directory and copy web files to the Apache document root
mkdir -p /var/www/html/temperature
cp html/index.php /var/www/html/temperature/
chown -R www-data:www-data /var/www/html/temperature

echo "Setup Complete!"
echo "You can now fetch data by running: python3 fetch_weather.py"
echo "View the dashboard at: http://localhost/temperature/index.php"
