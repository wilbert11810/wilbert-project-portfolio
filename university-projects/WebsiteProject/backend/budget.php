<?php
include "db.php";

header("Content-Type: application/json");
session_start();

$user_id = $_SESSION["user"]["id"];
$sql = "SELECT SUM(amount) AS totalSpent FROM finance WHERE user_id = ? AND MONTH(date) = MONTH(CURRENT_DATE())";
$stmt = $conn->prepare($sql);
$stmt->bind_param("i", $user_id);
$stmt->execute();
$result = $stmt->get_result();
$data = $result->fetch_assoc();

echo json_encode(["totalSpent" => isset($data["totalSpent"]) ? $data["totalSpent"] : 0]);

?>
