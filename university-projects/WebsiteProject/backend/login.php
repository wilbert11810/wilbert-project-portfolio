<?php
include "db.php";
session_start();

header("Content-Type: application/json");

$data = json_decode(file_get_contents("php://input"), true);
$email = isset($data["email"]) ? $data["email"] : "";
$password = isset($data["password"]) ? $data["password"] : "";


if (!$data || !isset($data["email"]) || !isset($data["password"])) {
    echo json_encode(["error" => "Invalid JSON request","raw_received" => $data_raw,
	"decoded_data" => $data ]);
    exit();
}


$sql = "SELECT * FROM users WHERE email = ?";
$stmt = $conn->prepare($sql);
$stmt->bind_param("s", $email);
$stmt->execute();
$result = $stmt->get_result();
$user = $result->fetch_assoc();
if (!$user) {
    echo json_encode(["error" => "User not found"]); 
    exit();
}

if ($password !== $user["password_hash"] ) {
    echo json_encode(["error" => "Incorrect password"]); 
    exit();
}
if ($user && $password === $user["password_hash"]) {
    $_SESSION["user"] = $user;
    echo json_encode(["message" => "Login successful!", "user" => $user]);
}
?>
