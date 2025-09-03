<?php
include "db.php";
session_start();

header("Content-Type: application/json");

if (!isset($_SESSION["user"])) {
    echo json_encode(["error" => "Unauthorized"]);
    exit();
}

$user_id = $_SESSION["user"]["id"];
$data = json_decode(file_get_contents("php://input"), true);

$sql = "UPDATE finance SET title=?, amount=?, category=?, date=?, notes=? WHERE id=? AND user_id=?";
$stmt = $conn->prepare($sql);
$stmt->bind_param("sdsssii", $data["title"], $data["amount"], $data["category"], $data["date"], $data["notes"], $data["expense_id"], $user_id);
$stmt->execute();

echo json_encode(["message" => "Expense updated successfully!"]);
?>
