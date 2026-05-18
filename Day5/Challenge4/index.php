<?php
/**
 * Raspberry Pi Temperature Recorder
 * This script connects to a local MySQL database, retrieves temperature records,
 * and displays them in a neatly formatted HTML table.
 */

// 1. Database Credentials
// Update these variables if your database configuration differs.
$host     = 'localhost';
$dbname   = 'iot_database';
$username = 'iot_user';     // Set to 'root' or 'iot_user' as per your setup
$password = '';             // Password for the database user

// Variables to hold our fetched data and any potential error messages
$temperature_data = [];
$error_message = '';

try {
    // 2. Establish Secure Database Connection using PDO
    $dsn = "mysql:host=$host;dbname=$dbname;charset=utf8mb4";
    
    // Set PDO options for error handling and fetching mechanisms
    $options = [
        PDO::ATTR_ERRMODE            => PDO::ERRMODE_EXCEPTION, // Throw exceptions on errors
        PDO::ATTR_DEFAULT_FETCH_MODE => PDO::FETCH_ASSOC,       // Fetch associative arrays
        PDO::ATTR_EMULATE_PREPARES   => false,                  // Use native prepared statements
    ];
    
    // Create the PDO instance
    $pdo = new PDO($dsn, $username, $password, $options);
    
    // 3. Data Retrieval
    // Fetch all rows from the temperature_log table, ordering by most recent first
    $sql = "SELECT sr_no, rec_time, rec_temp FROM temperature_log ORDER BY rec_time DESC";
    $stmt = $pdo->query($sql);
    
    // Store the results in our array
    $temperature_data = $stmt->fetchAll();

} catch (PDOException $e) {
    // Handle database connection or query errors gracefully
    // For security, don't expose raw stack traces. Show a user-friendly message.
    $error_message = "Failed to connect to the database or retrieve data. Please check your connection, credentials, and ensure the table exists.";
    // In a real production environment, you might log $e->getMessage() to a secure file here.
}
?>
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Raspberry Pi Temperature Recorder</title>
    <style>
        /* 4. Styling (Internal CSS) */
        body {
            font-family: "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
            background-color: #f4f7f6;
            margin: 0;
            padding: 40px;
            color: #333;
        }
        .container {
            max-width: 800px;
            margin: 0 auto;
            background-color: #ffffff;
            padding: 20px 30px;
            border-radius: 8px;
            box-shadow: 0 4px 8px rgba(0,0,0,0.1);
        }
        h1 {
            text-align: center;
            color: #2c3e50;
            margin-bottom: 20px;
        }
        .error-message {
            background-color: #f8d7da;
            color: #721c24;
            border: 1px solid #f5c6cb;
            padding: 15px;
            border-radius: 4px;
            margin-bottom: 20px;
            text-align: center;
        }
        table {
            width: 100%;
            border-collapse: collapse;
            margin-top: 10px;
        }
        th, td {
            border: 1px solid #ddd;
            padding: 12px 15px;
            text-align: center;
        }
        th {
            background-color: #3498db;
            color: #ffffff;
            font-weight: 600;
        }
        /* Alternating row colors */
        tr:nth-child(even) {
            background-color: #f9f9f9;
        }
        tr:hover {
            background-color: #f1f1f1;
        }
        .empty-state {
            color: #7f8c8d;
            font-style: italic;
            padding: 20px !important;
        }
    </style>
</head>
<body>

<div class="container">
    <!-- Page Title & Header -->
    <h1>Raspberry Pi Temperature Recorder</h1>

    <!-- Display Graceful Error Message if needed -->
    <?php if (!empty($error_message)): ?>
        <div class="error-message">
            <?php echo htmlspecialchars($error_message, ENT_QUOTES, 'UTF-8'); ?>
        </div>
    <?php endif; ?>

    <!-- Data Table -->
    <table>
        <thead>
            <tr>
                <th>No.</th>
                <th>Date and Time</th>
                <th>Temperature</th>
            </tr>
        </thead>
        <tbody>
            <?php if (empty($error_message)): ?>
                <?php if (count($temperature_data) > 0): ?>
                    <!-- Loop through records and generate table rows -->
                    <?php foreach ($temperature_data as $row): ?>
                        <tr>
                            <!-- Using htmlspecialchars for Security & Sanitation (preventing XSS) -->
                            <td><?php echo htmlspecialchars($row['sr_no'], ENT_QUOTES, 'UTF-8'); ?></td>
                            <td><?php echo htmlspecialchars($row['rec_time'], ENT_QUOTES, 'UTF-8'); ?></td>
                            <td><?php echo htmlspecialchars($row['rec_temp'], ENT_QUOTES, 'UTF-8'); ?> &deg;C</td>
                        </tr>
                    <?php endforeach; ?>
                <?php else: ?>
                    <!-- Empty State -> 0 records found -->
                    <tr>
                        <td colspan="3" class="empty-state">No temperature data found.</td>
                    </tr>
                <?php endif; ?>
            <?php else: ?>
                <!-- If there was an error, just display an empty state below headers -->
                <tr>
                    <td colspan="3" class="empty-state">Data unavailable due to a connection error.</td>
                </tr>
            <?php endif; ?>
        </tbody>
    </table>
</div>

</body>
</html>
