#!/bin/bash

# Configuration
DB_NAME="iot_database"
DB_USER="root"

echo "Database Initialization Script"
echo "------------------------------"

# Prompt for the MySQL root password securely
read -s -p "Enter MySQL password for user '$DB_USER': " DB_PASS
echo ""
echo "Initializing..."

# Execute the SQL commands to create the database and table
mysql -u "$DB_USER" -p"$DB_PASS" -e "
CREATE DATABASE IF NOT EXISTS $DB_NAME;
USE $DB_NAME;

CREATE TABLE IF NOT EXISTS temperature_log (
    sr_no INT AUTO_INCREMENT PRIMARY KEY,
    rec_time DATETIME DEFAULT CURRENT_TIMESTAMP,
    rec_temp FLOAT NOT NULL
);
"

# Check if the mysql command was successful
if [ $? -eq 0 ]; then
    echo "✅ Database '$DB_NAME' and table 'temperature_log' initialized successfully!"
else
    echo "❌ Failed to initialize the database. Please check your password and ensure MySQL/MariaDB is running."
fi
