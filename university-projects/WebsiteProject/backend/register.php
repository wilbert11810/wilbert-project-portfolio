<?php
include "db.php";

header("Content-Type: application/json");

$data = json_decode(file_get_contents("php://input"), true);
$first_name = $data["first_name"];
$last_name = $data["last_name"];
$email = $data["email"];
$password = $data["password"];


$sql = "INSERT INTO users (first_name, last_name, email, password_hash) VALUES (?, ?, ?, ?)";
$stmt = $conn->prepare($sql);
$stmt->bind_param("ssss", $first_name, $last_name, $email, $password);

if ($stmt->execute()) {
    echo json_encode(["message" => "User registered successfully!", "success" => true]);
} else {
    echo json_encode(["error" => "Registration failed"]);
}
?>
