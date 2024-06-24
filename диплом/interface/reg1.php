<?php
if ($_SERVER["REQUEST_METHOD"] == "POST") {
    $servername = "localhost";
    $username_db = "root"; 
    $password_db = "root"; 
    $dbname = "forecast_price";

    $conn = new mysqli($servername, $username_db, $password_db, $dbname);

    if ($conn->connect_error) {
        die("Connection failed: " . $conn->connect_error);
    }

    $username = $_POST['username'];
    $email = $_POST['email'];
    $pass = $_POST['pass'];

    if (empty($username) || empty($email) || empty($pass)) {
        die("Please fill in all fields.");
    }

    $hashed_password = password_hash($pass, PASSWORD_DEFAULT);

    $sql_registration = "INSERT INTO registration (username, email, pass) VALUES ('$username', '$email', '$hashed_password')";
    if ($conn->query($sql_registration) === TRUE) {
        $user_id = $conn->insert_id;

        $sql_user_profile = "INSERT INTO user_profile (UserId, username, email, pass) VALUES ('$user_id', '$username', '$email', '$hashed_password')";
        if ($conn->query($sql_user_profile) === TRUE) {
            header("Location: log.php ");
            exit();
        } else {
            die("Error: " . $sql_user_profile . "<br>" . $conn->error);
        }
    } else {
        die("Error: " . $sql_registration . "<br>" . $conn->error);
    }

    $conn->close();
}
?>




