# Day 5: HKO Temperature Monitor via Local MySQL/Apache Server

This module runs a full LAMP/LEMP-style stack setup optimized for a Raspberry Pi 4 environment.

## 1. Setup Instructions
To avoid permission issues over the OS, a setup script is provided.

```bash
cd day5
chmod +x setup.sh

# ONLY run this if permissions allow you to install system packages on the Pi natively.
# sudo ./setup.sh
```

**What the setup script does:**
1. Installs `mariadb-server` (The standard optimized counterpart to MySQL for RPi), `apache2`, `php`, and associated database extensions (`php-mysql`, `python3-pymysql`).
2. Enables and starts the services.
3. Automatically sets up the `schema.sql` (Creates `temperature_db` and user `pi_user`).
4. Moves the dashboard files to `/var/www/html/temperature`.

## 2. Populating Data
Run the python script iteratively or set it up via `crontab` to maintain a live feed of Hong Kong observatory reading snapshots.

```bash
python3 fetch_weather.py
```
> *Using `python3` instead of depreciated python2.* Let it populate data.

## 3. Viewing the Data Dashboard
Open a browser (on the Raspberry Pi or on the same network).
- Open: `http://localhost/temperature/index.php` (if viewing from the Pi)
- Or: `http://<RASPBERRY_PI_IP_ADDRESS>/temperature/index.php`

### Security and Standard Audit Notes:
* **`mysql_` vs `PDO`**: Old `mysql_*` syntax in PHP has been removed and inherently unsecure. We utilized standard PHP Data Objects (`PDO`) with exception error modes for clean runtime error traces.
* **SQL Injection Resiliency**: Prepared statements were explicitly used in Python insertion via `pymysql`. `PDO::ATTR_EMULATE_PREPARES` is set to false in PHP which securely protects the system.
* **XSS Mitigation**: `htmlspecialchars` has fully encapsulated array outputs inside the final HTML template render. 
* **Database Driver**: Leveraging `mariadb-server` ensures compliance via `apt` with Debian distributions matching Raspberry Pi OS constraints.