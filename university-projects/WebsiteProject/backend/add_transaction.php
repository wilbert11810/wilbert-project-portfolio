<?php
include "db.php";
session_start();
header("Content-Type: application/json");

if (!isset($_SESSION["user"])) {
    echo json_encode(["error" => "Unauthorized access"]);
    exit();
}

$user_id = $_SESSION["user"]["id"];
$data = json_decode(file_get_contents("php://input"), true);

if (empty($data["title"]) || empty($data["amount"]) || empty($data["date"]) || empty($data["category"])) {
    echo json_encode(["error" => "Invalid data"]);
    exit();
}

$sql = "INSERT INTO finance (user_id, title, amount, date, category, notes) VALUES (?, ?, ?, ?, ?, ?)";
$stmt = $conn->prepare($sql);
$stmt->bind_param("isdsss", $user_id, $data["title"], $data["amount"], $data["date"], $data["category"], $data["notes"]);
$stmt->execute();

echo json_encode(["success" => true, "message" => "Transaction added successfully!"]);
?>
