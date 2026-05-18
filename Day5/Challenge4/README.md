# Raspberry Pi Temperature Web Dashboard

This project contains a PHP-based web dashboard (`index.php`) that connects to a local MySQL database to display temperature data logged by the Sense HAT. 

Follow the instructions below to configure your Raspberry Pi to serve this webpage.

## Prerequisites
To host a PHP webpage that talks to a MySQL database, your Raspberry Pi needs a web server (Apache) and the PHP processing language equipped with MySQL extensions.

If you haven't installed them yet, open your terminal and run:
```bash
sudo apt update
sudo apt install apache2 php libapache2-mod-php php-mysql
```

## Deployment Instructions

### 1. Copy the file to the Apache Web Root
By default, Apache serves public web files from the `/var/www/html/` directory. You need to copy our `index.php` file into this directory.

Run the following command from the root of this project:
```bash
# Copy index.php to the Apache web directory
sudo cp index.php /var/www/html/
```
*(Note: If Apache already put a default `index.html` file in there, you might want to remove it using `sudo rm /var/www/html/index.html` so it doesn't conflict with your new PHP page).*

### 2. Restart Apache
After installing new PHP extensions or making major changes, it is good practice to restart the Apache service:
```bash
sudo systemctl restart apache2
```

## Accessing the Webpage

Now that the file is in place and the server is running, you can view your temperature dashboard!

### View from the Raspberry Pi directly:
Open a web browser (like Chromium) on the Raspberry Pi and navigate to:
* `http://localhost`

### View from another device (Laptop, Phone, etc.):
To view the site from another computer on the same Wi-Fi network, you need your Raspberry Pi's IP address.
1. Find your IP address by running this command in the Pi's terminal:
   ```bash
   hostname -I
   ```
2. Open a web browser on your other device and type in that IP address. For example:
   * `http://192.168.1.50`

You should now see the "Raspberry Pi Temperature Recorder" dashboard displaying the rows of data retrieved dynamically from your local MySQL database.
