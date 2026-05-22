-- Database schema for Hong Kong Temperature Records
-- Compatible with MySQL and MariaDB

CREATE DATABASE IF NOT EXISTS temperature_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE temperature_db;

-- 1. Create the main temperature records table
-- Using InnoDB for reliability and ACID compliance
CREATE TABLE IF NOT EXISTS temperature_records (
    id INT AUTO_INCREMENT PRIMARY KEY,
    record_time DATETIME DEFAULT CURRENT_TIMESTAMP,
    location VARCHAR(100) NOT NULL,
    temperature DECIMAL(5,2) NOT NULL,
    INDEX idx_record_time (record_time)
) ENGINE=InnoDB;

-- 2. Create an isolated database user for the application
-- It is bad practice to use root for application queries
CREATE USER IF NOT EXISTS 'pi_user'@'localhost' IDENTIFIED BY 'pi_password';

-- 3. Grant permissions only for this specific database
GRANT SELECT, INSERT ON temperature_db.* TO 'pi_user'@'localhost';

-- Apply privileges
FLUSH PRIVILEGES;