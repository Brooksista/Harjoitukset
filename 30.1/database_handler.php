<?php

// Debugging: Output the received parameters

$servername = "localhost";
$username = "root";
$password = "kukkula";
$dbname = "tilavaraus";

$conn = new mysqli($servername, $username, $password, $dbname);
if ($conn->connect_error) die("Connection failed: " . $conn->connect_error);

// Allowed tables
$allowedTables = ["tilat", "varaajat", "varaukset"];
$table = $_GET['table'] ?? '';
if (!in_array($table, $allowedTables)) {
    echo json_encode(['success' => false, 'message' => 'Invalid table selected']);
    exit;
}

// Actions
$action = $_GET['action'] ?? '';
if ($action == 'view') {
    $result = $conn->query("SELECT * FROM $table");
    $data = [];
    while ($row = $result->fetch_assoc()) $data[] = $row;
    echo json_encode($data);

} elseif ($action == 'add') {
    if ($table == 'tilat') {
        $name = $_POST['tilan_nimi'] ?? '';
        $stmt = $conn->prepare("INSERT INTO tilat (tilan_nimi) VALUES (?)");
        $stmt->bind_param("s", $name);
    } elseif ($table == 'varaajat') {
        $name = $_POST['nimi'] ?? '';
        $stmt = $conn->prepare("INSERT INTO varaajat (nimi) VALUES (?)");
        $stmt->bind_param("s", $name);
    } elseif ($table == 'varaukset') {
        $tila = $_POST['tila'] ?? 0;
        $varaaja = $_POST['varaaja'] ?? 0;
        $date = $_POST['varauspaiva'] ?? '';
        $stmt = $conn->prepare("INSERT INTO varaukset (tila, varaaja, varauspaiva) VALUES (?, ?, ?)");
        $stmt->bind_param("iis", $tila, $varaaja, $date);
    }
    $stmt->execute();
    echo json_encode(['success' => $stmt->affected_rows > 0, 'message' => $stmt->affected_rows > 0 ? 'Record added successfully' : 'Failed to add record']);
    $stmt->close();

} elseif ($action == 'delete') {
    $id = $_POST['id'] ?? 0;
    $stmt = $conn->prepare("DELETE FROM $table WHERE id = ?");
    $stmt->bind_param("i", $id);
    $stmt->execute();
    echo json_encode(['success' => $stmt->affected_rows > 0, 'message' => $stmt->affected_rows > 0 ? 'Record deleted successfully' : 'Failed to delete record']);
    $stmt->close();
}

$conn->close();
?>
