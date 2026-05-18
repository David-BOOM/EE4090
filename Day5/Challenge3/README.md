# Sense HAT Temperature Logger

This project reads real-time temperature data from a Raspberry Pi Sense HAT and logs it to a local MySQL database.

## Prerequisites

### Hardware
* Raspberry Pi
* Sense HAT module attached to the GPIO pins

### Software & Libraries
* Python 3
* MySQL Server (local)
* `sense-hat` Python package
* `mysqlclient` Python package

You can install the necessary dependencies on your Raspberry Pi using the following commands:
```bash
sudo apt-get update
sudo apt-get install sense-hat python3-dev default-libmysqlclient-dev build-essential
pip3 install mysqlclient
```

## Setup Instructions

### 1. Database Setup
First, make sure your MySQL server is running. Then, create the necessary database and table using the provided `schema.sql` file. From your terminal, run:

```bash
# Create a database (if you don't already have one)
mysql -u root -p -e "CREATE DATABASE IF NOT EXISTS iot_database;"

# Import the table schema into the database
mysql -u root -p iot_database < schema.sql
```

### 2. Configure the Script
Before running the script, you must configure it with your database credentials. Open `log_temperature.py` and update the `db_config` section:

```python
db_config = {
    "host": "localhost",
    "user": "root",           # Replace with your MySQL username
    "passwd": "your_password",# Replace with your MySQL password
    "db": "iot_database"      # Ensure this matches your target database
}
```

### 3. Run the Tracker
Once configured, you can run the script manually to log a single temperature reading:

```bash
python3 log_temperature.py
```

### Automating the Script (Optional)
If you want to log the temperature automatically at set intervals (e.g., every 5 minutes), you can add a cron job:
```bash
crontab -e
```
Add the following line at the bottom of the file (update the path to match the script's location):
```bash
*/5 * * * * /usr/bin/python3 /home/pi/Projects/EE4090/Day5/Challenge3/log_temperature.py
```
