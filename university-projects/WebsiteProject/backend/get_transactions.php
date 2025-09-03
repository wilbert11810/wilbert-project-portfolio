<?php
include "db.php";
session_start();
header("Content-Type: application/json");

if (!isset($_SESSION["user"])) {
    echo json_encode(array("error" => "Unauthorized access"));
    exit();
}

$user_id   = $_SESSION["user"]["id"];
$page      = isset($_GET["page"]) ? (int)$_GET["page"] : 1;
$perPage   = isset($_GET["perPage"]) ? (int)$_GET["perPage"] : 5;
$sortBy    = isset($_GET["sortBy"]) ? $_GET["sortBy"] : "date";
$category  = isset($_GET["category"]) ? $_GET["category"] : "";
$startDate = isset($_GET["startDate"]) ? $_GET["startDate"] : "";
$endDate   = isset($_GET["endDate"]) ? $_GET["endDate"] : "";
$search    = isset($_GET["search"]) ? $_GET["search"] : "";

$baseSql    = " FROM finance WHERE user_id = ?";
$paramTypes = "i";
$params     = array($user_id);



if ($category) {
    $baseSql    .= " AND category = ?";
    $paramTypes .= "s";
    $params[]    = $category;
}



if ($startDate && $endDate) {
    $baseSql    .= " AND date BETWEEN ? AND ?";
    $paramTypes .= "ss";
    $params[]    = $startDate;
    $params[]    = $endDate;
}

if ($search) {
    $baseSql    .= " AND title LIKE ?";
    $paramTypes .= "s";
    $params[]    = "%$search%";
}


$countSql = "SELECT COUNT(*) as total" . $baseSql;
$stmtCount = $conn->prepare($countSql);
if ($stmtCount === false) {
    echo json_encode(array("error" => "Database error: " . $conn->error));
    exit();
}


$bind_names = array();
$bind_names[] = $paramTypes;
foreach ($params as $key => $value) {
    $bind_names[] = &$params[$key];
}
call_user_func_array(array($stmtCount, 'bind_param'), $bind_names);

$stmtCount->execute();
$resultCount = $stmtCount->get_result();
$totalRecords = 0;
if ($row = $resultCount->fetch_assoc()) {
    $totalRecords = $row['total'];
}
$stmtCount->close();


$mainSql = "SELECT *" . $baseSql . " ORDER BY $sortBy DESC LIMIT ?, ?";

$mainParamTypes = $paramTypes . "ii";
$offset = ($page - 1) * $perPage;
$mainParams = $params; 
$mainParams[] = $offset;
$mainParams[] = $perPage;

$stmt = $conn->prepare($mainSql);

if ($stmt === false) {
    echo json_encode(array("error" => "Database error: " . $conn->error));
    exit();
}


$bind_names_main = array();
$bind_names_main[] = $mainParamTypes;
foreach ($mainParams as $key => $value) {
    $bind_names_main[] = &$mainParams[$key];
}
call_user_func_array(array($stmt, 'bind_param'), $bind_names_main);


$stmt->execute();
if (!$stmt->execute()) {
    echo json_encode(array("error" => "Database error: " . $stmt->error));
    exit();
}
$result = $stmt->get_result();

$transactions = array();
while ($row = $result->fetch_assoc()) {
    $transactions[] = $row;
}
$stmt->close();

echo json_encode(array(
    "transactions" => $transactions,
    "totalRecords" => $totalRecords,
    "totalPages"   => ceil($totalRecords / $perPage)
));
?>
