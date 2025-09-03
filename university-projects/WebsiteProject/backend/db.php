<?php 
    $host = "feenix-mariadb.swin.edu.au";
	$username = "s104323659"; 
	$password = "010704"; 
	$dbname = "s104323659_db";

    $conn = new mysqli($host, $username, $password, $dbname);

    if ($conn-> connect_error) {
        die("Connection failed: " . $conn-> connect_error);
    }
?>
   
