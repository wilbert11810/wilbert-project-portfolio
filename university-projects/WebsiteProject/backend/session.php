<?php
include "db.php";
session_start(); 

header("Content-Type: application/json");

if (isset($_SESSION["user"])) {
    echo json_encode(["user" => $_SESSION["user"]]);
} else {
    echo json_encode(["error" => "No active session"]);
}
?>
