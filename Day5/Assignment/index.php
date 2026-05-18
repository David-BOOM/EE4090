<?php
/**
 * Stage 1: Environment Recorder Display
 * This script retrieves data from the local_env_records table and
 * securely outputs the dataset on a clean web interface.
 */

// Prevent browser caching to ensure fresh data is always displayed
header("Cache-Control: no-store, no-cache, must-revalidate, max-age=0");
header("Cache-Control: post-check=0, pre-check=0", false);
header("Pragma: no-cache");

// 1. Database Configuration
$host = 'localhost';
$dbname = 'mydb';
$username = 'iot_user'; // Swap to 'iot_user' depending on the Pi's user configurations
$password = '';   

$env_data = [];
$error_message = '';

try {
    // 2. Establish Secure connection using PDO
    $dsn = "mysql:host=$host;dbname=$dbname;charset=utf8mb4";
    $options = [
        PDO::ATTR_ERRMODE            => PDO::ERRMODE_EXCEPTION,
        PDO::ATTR_DEFAULT_FETCH_MODE => PDO::FETCH_ASSOC,
        PDO::ATTR_EMULATE_PREPARES   => false,
    ];
    $pdo = new PDO($dsn, $username, $password, $options);
    
    // 3. Fetch Records
    // Ordering by rec_time descending logic places the newest recordings at the top
    $sql = "SELECT ID, rec_time, rec_temp, rec_humi, rec_press FROM local_env_records ORDER BY rec_time DESC";
    $stmt = $pdo->query($sql);
    $env_data = $stmt->fetchAll();

} catch (PDOException $e) {
    // Graceful error layout catching if database fails
    $error_message = "Unable to connect to the database. Please check your config and ensure the table exists.";
}
?>
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <!-- Auto-refresh the page every 3 seconds to fetch new data -->
    <meta http-equiv="refresh" content="3">
    <title>Raspberry Pi Environment Recorder</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            margin: 40px;
            background-color: #f7f9fc;
            color: #333;
        }
        .container {
            max-width: 900px;
            margin: auto;
            background: white;
            padding: 20px 30px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
            border-radius: 8px;
        }
        h1 {
            text-align: center;
            color: #4CAF50;
        }
        .error {
            background: #ffdddd;
            color: #d8000c;
            border-left: 5px solid #f44336;
            padding: 15px;
            margin-bottom: 20px;
        }
        table {
            width: 100%;
            border-collapse: collapse;
            margin-top: 20px;
        }
        th, td {
            text-align: center;
            padding: 12px;
            border: 1px solid #ddd;
        }
        th {
            background-color: #4CAF50;
            color: white;
        }
        tr:nth-child(even) {
            background-color: #f2f2f2;
        }
    </style>
</head>
<body>

<div class="container">
    <h1>Raspberry Pi Environment Recorder</h1>

    <?php if ($error_message): ?>
        <div class="error"><?php echo htmlspecialchars($error_message, ENT_QUOTES, 'UTF-8'); ?></div>
    <?php endif; ?>

    <table>
        <thead>
            <tr>
                <th>ID</th>
                <th>Date and Time</th>
                <th>Temperature</th>
                <th>Humidity</th>
                <th>Pressure</th>
            </tr>
        </thead>
        <tbody>
            <?php if (empty($error_message)): ?>
                <?php if (count($env_data) > 0): ?>
                    <?php foreach ($env_data as $row): ?>
                        <tr>
                            <!-- Escaping output to stop Cross-Site Scripting (XSS) -->
                            <td><?php echo htmlspecialchars($row['ID'], ENT_QUOTES, 'UTF-8'); ?></td>
                            <td><?php echo htmlspecialchars($row['rec_time'], ENT_QUOTES, 'UTF-8'); ?></td>
                            <td><?php echo htmlspecialchars($row['rec_temp'], ENT_QUOTES, 'UTF-8'); ?> &deg;C</td>
                            <td><?php echo htmlspecialchars($row['rec_humi'], ENT_QUOTES, 'UTF-8'); ?> %</td>
                            <td><?php echo htmlspecialchars($row['rec_press'], ENT_QUOTES, 'UTF-8'); ?> hPa</td>
                        </tr>
                    <?php endforeach; ?>
                <?php else: ?>
                    <tr>
                        <td colspan="5">No environment data found.</td>
                    </tr>
                <?php endif; ?>
            <?php else: ?>
                <tr>
                    <td colspan="5">Connection Error. Data invisible.</td>
                </tr>
            <?php endif; ?>
        </tbody>
    </table>
</div>

</body>
</html>
