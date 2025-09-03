<?php
include "db.php";
session_start();
header("Content-Type: application/json");

if (!isset($_SESSION["user"])) {
    echo json_encode(["error" => "Unauthorized access"]);
    exit();
}

$user_id = $_SESSION["user"]["id"];


$selectedMonth = isset($_GET["month"]) ? $_GET["month"] : "";
$selectedCategory = isset($_GET["category"]) ? $_GET["category"] : "";


$whereClause = "WHERE user_id = ?";
$paramTypes = "i";
$params = [$user_id];


if (!empty($selectedCategory)) {
    $whereClause .= " AND category = ?";
    $paramTypes .= "s";
    $params[] = $selectedCategory;
}

if (!empty($selectedMonth)) {
    $whereClause .= " AND DATE_FORMAT(date, '%Y-%m') = ?";
    $paramTypes .= "s";
    $params[] = $selectedMonth;
}

$sql = "SELECT category, SUM(amount) AS total_amount FROM finance $whereClause GROUP BY category";
$stmt = $conn->prepare($sql);
if ($stmt === false) {
    echo json_encode(array("error" => "Database error (prepare failed)"));
    exit();
}


$bind_names = array();
$bind_names[] = $paramTypes;
for ($i = 0; $i < count($params); $i++) {
    $bind_names[] = &$params[$i];
}

call_user_func_array(array($stmt, 'bind_param'), $bind_names);
$stmt->execute();
$result = $stmt->get_result();

$visualizationData = [];
while ($row = $result->fetch_assoc()) {
    $visualizationData[$row["category"]] = $row["total_amount"];
}

$sql2 = "SELECT DISTINCT date FROM finance WHERE user_id = ? ORDER BY date DESC";
$stmt2 = $conn->prepare($sql2);
$stmt2->bind_param("i", $user_id);
$stmt2->execute();
$result2 = $stmt2->get_result();

$transactions = [];
while ($row = $result2->fetch_assoc()) {
    $transactions[] = $row;
}

echo json_encode([
    "visualizationData" => $visualizationData,
    "transactions" => $transactions
]);
?>
