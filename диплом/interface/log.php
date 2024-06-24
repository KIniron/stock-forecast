<?php
session_start();

if ($_SERVER["REQUEST_METHOD"] == "POST") {
    // Підключення до бази даних
    $servername = "localhost";
    $username = "root"; 
    $password = "root"; 
    $dbname = "forecast_price";

    
    $conn = new mysqli($servername, $username, $password, $dbname);

    
    if ($conn->connect_error) {
        die("Connection failed: " . $conn->connect_error);
    }

    
    $username = $_POST['username'];
    $password = $_POST['password'];

    
    $sql = "SELECT * FROM user_profile WHERE username = ?";
    $stmt = $conn->prepare($sql);
    $stmt->bind_param("s", $username);
    $stmt->execute();
    $result = $stmt->get_result();
    $row = $result->fetch_assoc();

    if ($row && password_verify($password, $row['pass'])) {
        
        $_SESSION['userID'] = $row['UserID'];
        header("Location: intro.php");
        exit();
    } else {
        
        $login_error = "Invalid username or password";
    }

    // Закриття підключення до бази даних
    $conn->close();
}
?>

<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link rel="stylesheet" href="style2.css">
    <title>Login</title>
</head>
<body>
<div class="right-container">
                    <nav class="nav">
                    <a class="nav__link" href="intro.php">Головна</a>
                     <a class="nav__link" href="http://localhost:8050">Прогнозування акцій</a>  
                        <a class="nav__link" href="Cont.php">Зворотній зв'язок</a>
                        
                        
                    <?php
                        if (isset($_SESSION['userID'])) {
                            echo '<a class="login-button" href="logout.php">Вийти</a>';
                        } else {
                            echo '<a class="login-button" href="log.php">Увійти</a>';
                        }
                        echo '<a class="reg-button" href="reg.php">Зараєструватись</a>';
                    ?>
                    </nav>
                </div>
    
    <form action="<?php echo htmlspecialchars($_SERVER["PHP_SELF"]); ?>" method="post">
    <h2>Вхід в акаунт</h2>
        <label for="username">Нік:</label>
        <input type="text" id="username" name="username" required><br><br>
        <label for="password">Пароль:</label>
        <input type="password" id="password" name="password" required><br><br>
        <button type="submit">увійти</button>
        
    </form>
    <?php if(isset($login_error)) { echo "<p>$login_error</p>"; } ?>
</body>
</html>

