-- Create the target database (if it doesn't already exist)
CREATE DATABASE IF NOT EXISTS mydb;
USE mydb;

-- Stage 1 Local Database Table
-- Notice that we use ID as an INT for the Pi identifying number, 
-- and rec_time defaults to the local server timestamp.
CREATE TABLE IF NOT EXISTS local_env_records (
    ID INT NOT NULL,
    rec_time DATETIME DEFAULT CURRENT_TIMESTAMP,
    rec_temp FLOAT NOT NULL,
    rec_humi FLOAT NOT NULL,
    rec_press FLOAT NOT NULL
);

-- Stage 2 Training Database Tables
-- Table schemas to be used for the Joystick event-driven script
CREATE TABLE IF NOT EXISTS trainingdb1 (
    ID INT NOT NULL,
    rec_time DATETIME DEFAULT CURRENT_TIMESTAMP,
    rec_temp FLOAT NOT NULL,
    rec_humi FLOAT NOT NULL,
    rec_press FLOAT NOT NULL
);

CREATE TABLE IF NOT EXISTS trainingdb2 (
    ID INT NOT NULL,
    rec_time DATETIME DEFAULT CURRENT_TIMESTAMP,
    rec_temp FLOAT NOT NULL,
    rec_humi FLOAT NOT NULL,
    rec_press FLOAT NOT NULL
);
