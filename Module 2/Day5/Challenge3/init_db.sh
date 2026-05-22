#!/bin/bash

# Configuration
DB_NAME="iot_database"
DB_USER="root"

echo "Database Initialization Script"
echo "------------------------------"
echo "Initializing..."

# Execute the SQL commands to create the database, user, and table
sudo mysql -u "$DB_USER" -e "
CREATE DATABASE IF NOT EXISTS $DB_NAME;
CREATE USER IF NOT EXISTS 'iot_user'@'localhost' IDENTIFIED BY '';
GRANT ALL PRIVILEGES ON $DB_NAME.* TO 'iot_user'@'localhost';
FLUSH PRIVILEGES;
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
