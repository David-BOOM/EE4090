<?php
/**
 * Hong Kong Temperature Monitor Dashboard
 * Uses PDO to securely connect to the local MariaDB/MySQL database.
 */

// 1. Configuration Constants
$host = 'localhost';
$db   = 'temperature_db';
$user = 'pi_user';
$pass = 'pi_password';
$charset = 'utf8mb4';

// 2. PDO Data Source Name (DSN) setup
$dsn = "mysql:host=$host;dbname=$db;charset=$charset";

// 3. PDO Options:
// - ERRMODE_EXCEPTION: Secure error throwing
// - FETCH_ASSOC: Lends itself well to associative arrays arrays for rows
// - EMULATE_PREPARES false: Native database preparing limits SQL injection vectors
$options = [
    PDO::ATTR_ERRMODE            => PDO::ERRMODE_EXCEPTION,
    PDO::ATTR_DEFAULT_FETCH_MODE => PDO::FETCH_ASSOC,
    PDO::ATTR_EMULATE_PREPARES   => false,
];

try {
    // Attempt Database Connection
    $pdo = new PDO($dsn, $user, $pass, $options);
} catch (\PDOException $e) {
    // Graceful error termination (prevent leaking credentials to screen)
    die("Database connection failed. Please check server status locally. (Error Code: " . (int)$e->getCode() . ")");
}

// 4. Fetch the latest 50 records from the database
try {
    $stmt = $pdo->query('SELECT record_time, location, temperature FROM temperature_records ORDER BY record_time DESC LIMIT 50');
    $records = $stmt->fetchAll();
} catch (\PDOException $e) {
    $records = [];
}
?>
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>HKO Temperature Monitor</title>
    <style>
        :root {
            --bg-color: #f4f7f6;
            --container-bg: #ffffff;
            --text-color: #333333;
            --table-border: #e0e0e0;
            --header-bg: #0078D7;
            --header-text: #ffffff;
            --row-odd: #f9f9f9;
            --row-hover: #eef2f5;
        }

        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background-color: var(--bg-color);
            color: var(--text-color);
            margin: 0;
            padding: 20px;
            display: flex;
            justify-content: center;
        }

        .container {
            background-color: var(--container-bg);
            padding: 30px;
            border-radius: 8px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
            width: 100%;
            max-width: 900px;
        }

        h1 {
            color: var(--header-bg);
            border-bottom: 2px solid var(--header-bg);
            padding-bottom: 10px;
        }

        p.desc {
            color: #666;
            font-size: 0.95em;
        }

        table {
            width: 100%;
            border-collapse: collapse;
            margin-top: 20px;
        }

        th, td {
            padding: 12px 15px;
            text-align: left;
            border-bottom: 1px solid var(--table-border);
        }

        th {
            background-color: var(--header-bg);
            color: var(--header-text);
            font-weight: 600;
        }

        tr:nth-child(odd) {
            background-color: var(--row-odd);
        }

        tr:hover {
            background-color: var(--row-hover);
        }

        .no-data {
            text-align: center;
            font-style: italic;
            color: #888;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>Raspberry Pi Temperature Monitor</h1>
        <p class="desc">Displaying the most recent temperature snapshot recorded from the Hong Kong Observatory Open Data API.</p>
        
        <table>
            <thead>
                <tr>
                    <th>Timestamp</th>
                    <th>Location</th>
                    <th>Temperature (°C)</th>
                </tr>
            </thead>
            <tbody>
                <?php if (count($records) > 0): ?>
                    <?php foreach ($records as $row): ?>
                        <tr>
                            <!-- Security note: htmlspecialchars mitigates XSS attacks -->
                            <td><?= htmlspecialchars($row['record_time'], ENT_QUOTES, 'UTF-8') ?></td>
                            <td><?= htmlspecialchars($row['location'], ENT_QUOTES, 'UTF-8') ?></td>
                            <!-- Format temperature to consistently show 1 decimal place -->
                            <td><?= number_format((float)$row['temperature'], 1, '.', '') ?> °C</td>
                        </tr>
                    <?php endforeach; ?>
                <?php else: ?>
                    <tr>
                        <td colspan="3" class="no-data">No data found in the local database. Run the Python fetch script first.</td>
                    </tr>
                <?php endif; ?>
            </tbody>
        </table>
    </div>
</body>
</html>