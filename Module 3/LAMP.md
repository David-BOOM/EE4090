### Checkpoint 5:

```bash
# Enable the short open tag feature flags across all system php configuration files
for ini in $(find /etc/php/ -name php.ini); do
    sudo sed -i 's/short_open_tag = Off/short_open_tag = On/' $ini
done
sudo systemctl restart apache2

# Build the temporary dynamic guest log data repository with public write permissions
sudo touch /tmp/notes.txt && sudo chmod 777 /tmp/notes.txt

# Create the primary guestbook registration interface file
cat << 'EOF' | sudo tee /var/www/html/guest.php
<html>
<head><title>Network and System Administration - PHP Programming</title></head>
<body>
<h1>Welcome to my Guestbook</h1>
<h2>Please write me a little note below</h2>
<form action="<?echo $_SERVER['PHP_SELF']?>" method="POST">
<textarea cols=50 rows=8 name=note wrap=virtual></textarea><br>
<input type=submit value="Drop it down!">
</form>
<?
foreach ($_REQUEST as $key=>$val) { ${$key}=$val; }
if(isset($note) && !empty($note)){
    $fp=fopen("/tmp/notes.txt","a");
    fputs($fp,nl2br(htmlspecialchars($note)).'<br>');
    fclose($fp);
}
?>
<h2>The entries so far:</h2>
<? if(file_exists("/tmp/notes.txt")) readfile("/tmp/notes.txt"); ?>
</body>
</html>
EOF
```

---

### Checkpoint 6:

```bash
# 1. VISITOR COUNTER CODE DEPLOYMENT
sudo touch /var/www/html/counter001.txt && sudo chmod 777 /var/www/html/counter001.txt
cat << 'EOF' | sudo tee /var/www/html/counter001.php
<?php
$file = "/var/www/html/counter001.txt";
$count = file_exists($file) ? (int)file_get_contents($file) : 0;
$count++;
file_put_contents($file, $count);
echo "$count visitors";
?>
EOF
sudo chmod 644 /var/www/html/counter001.php

# Append the tracking script call into the guestbook
if ! grep -q "counter001.php" /var/www/html/guest.php; then
    echo "<br><? include('/var/www/html/counter001.php'); ?>" | sudo tee -a /var/www/html/guest.php
fi

# 2. FILE ACCESS PROTECTION MODULE
sudo sed -i '/<Directory \/var\/www\/>/,/<\/Directory>/s/AllowOverride None/AllowOverride All/' /etc/apache2/apache2.conf
sudo mkdir -p /var/www/html/secure
sudo htpasswd -cb /etc/apache2/.htpasswd student linux4095

cat << 'EOF' | sudo tee /var/www/html/secure/.htaccess
AuthType Basic
AuthName "Secure Area"
AuthUserFile /etc/apache2/.htpasswd
<Limit GET POST OPTIONS>
    Require valid-user
</Limit>
EOF
echo "<h1>Access Granted</h1>" | sudo tee /var/www/html/secure/index.html

# 3. LOCAL CGI ENGLISH-CHINESE DICTIONARY SYSTEM SETUP
sudo a2enmod cgi
sudo sed -i 's|ScriptAlias /cgi-bin/ /usr/lib/cgi-bin/|ScriptAlias /cgi-bin/ /var/www/cgi-bin/|g' /etc/apache2/conf-available/serve-cgi-bin.conf
sudo sed -i 's|<Directory "/usr/lib/cgi-bin">|<Directory "/var/www/cgi-bin">|g' /etc/apache2/conf-available/serve-cgi-bin.conf
sudo a2enconf serve-cgi-bin

sudo mkdir -p /var/www/cgi-bin/dict
sudo wget --no-check-certificate -O /tmp/dict.tar.gz https://www.ee.cityu.edu.hk/~ee4095/pdf/dict.tar.gz
sudo tar -xzf /tmp/dict.tar.gz -C /var/www/cgi-bin/dict/

# Flatten any nested folder structures extracted from the tar package
if [ -d /var/www/cgi-bin/dict/dict ]; then
    sudo mv /var/www/cgi-bin/dict/dict/* /var/www/cgi-bin/dict/ 2>/dev/null || true
    sudo rmdir /var/www/cgi-bin/dict/dict 2>/dev/null || true
fi

# Clean up hidden Windows carriage returns (\r) to fix database parsing failures
sudo sed -i 's/\r//g' /var/www/cgi-bin/dict/* 2>/dev/null || true

# Rewrite internal path configuration and target actions to run locally inside Apache
sudo sed -i 's|action\s*=\s*"[^"]*"|action="http://localhost/cgi-bin/dict/dict.cgi"|g' /var/www/cgi-bin/dict/dict.cgi 2>/dev/null || true
sudo sed -i 's|path\s*=\s*"[^"]*"|path="/var/www/cgi-bin/dict/"|g' /var/www/cgi-bin/dict/dict.cgi 2>/dev/null || true
sudo sed -i 's|"\$path/dict.txt"|"dict.txt"|g' /var/www/cgi-bin/dict/dict.cgi 2>/dev/null || true
sudo sed -i 's|"\$path/dict.dat"|"dict.dat"|g' /var/www/cgi-bin/dict/dict.cgi 2>/dev/null || true
sudo sed -i 's|\$path\s*\.\s*||g' /var/www/cgi-bin/dict/dict.cgi 2>/dev/null || true
sudo sed -i 's|http://[^"]*/dict.cgi|http://localhost/cgi-bin/dict/dict.cgi|g' /var/www/cgi-bin/dict/dict.cgi 2>/dev/null || true

# Standardize permissions configurations and reload service routing maps
sudo chmod -R 755 /var/www/cgi-bin/dict
sudo chmod +x /var/www/cgi-bin/dict/dict.cgi
sudo chown -R www-data:www-data /var/www/cgi-bin/dict
sudo systemctl restart apache2
```

---

### Checkpoint 7:

```bash
# Enable the user workspace server module
sudo a2enmod userdir

# Modify permissions rules configuration within the module directory mapping file
sudo sed -i 's/AllowOverride FileInfo AuthConfig Limit Indexes/AllowOverride All/g' /etc/apache2/mods-available/userdir.conf

# Confirm the target student Unix operating system shell profile exists
id -u student &>/dev/null || sudo useradd -m -s /bin/bash student
echo "student:linux4095" | sudo chpasswd

# Build target home content layout maps
sudo mkdir -p /home/student/public_html/info
echo "<h1>Student Home Page Working</h1>" | sudo tee /home/student/public_html/index.html
echo "<h1>Secure Info Folder Data</h1>" | sudo tee /home/student/public_html/info/index.html

# Apply access restrictions utilizing a explicit Limit declaration block mapping rules
cat << 'EOF' | sudo tee /home/student/public_html/info/.htaccess
AuthType Basic
AuthName "Student Secure Space"
AuthUserFile /etc/apache2/.htpasswd
<Limit GET POST OPTIONS>
    Require valid-user
</Limit>
EOF

# Grant traversal permission flags to Apache down the directory pathway
sudo chmod 755 /home/student
sudo chmod -R 755 /home/student/public_html
sudo chown -R student:student /home/student/public_html
sudo systemctl restart apache2
```

---

### Checkpoint 8:

```bash
# Create the dynamic random lottery generation engine script file
cat << 'EOF' | sudo tee /var/www/html/marksix.php
<html>
<head><title>Mark Six Predictor</title></head>
<body>
<h2>Mark Six Lucky Numbers Simulation:</h2>
<p style="font-size: 24px; color: green; font-weight: bold;">
<?php
$pool = range(1, 49);
shuffle($pool);
$selected = array_slice($pool, 0, 6);
sort($selected);
echo implode(" - ", $selected);
?>
</p>
</body>
</html>
EOF

sudo chmod 644 /var/www/html/marksix.php
```

---

### Checkpoint 9:

```bash
# Duplicate your counter executable tool into the student's active public workspace path
sudo cp /var/www/html/counter001.php /home/student/public_html/counter001.php
sudo chown student:student /home/student/public_html/counter001.php
sudo chmod 644 /home/student/public_html/counter001.php

# Fix Apache restriction rule that defaults PHP compilation off inside home workspaces (~user)
sudo sed -i '/<IfModule mod_userdir.c>/,/<\/IfModule>/s/php_admin_flag engine Off/php_admin_flag engine On/g' /etc/apache2/mods-available/php*.conf

# Ensure global write accessibility permissions for the counter counter storage file remains active
sudo touch /var/www/html/counter001.txt && sudo chmod 777 /var/www/html/counter001.txt

sudo systemctl restart apache2
```
