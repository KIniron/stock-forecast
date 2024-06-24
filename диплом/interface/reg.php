<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>User Registration</title>
    <link rel="stylesheet" href="style.css"> 
</head>
<body>
    <div class="navigation">
    <?php
                        if (isset($_SESSION['userID'])) {
                            echo '<a class="login-button" href="logout.php">Вийти</a>';
                        } else {
                            echo '<a class="login-button" href="log.php">Увійти</a>';
                        }
                        echo '<a class="reg-button" href="reg.php">Зараєструватись</a>';
                    ?>
        <a class="nav__link" href="intro.php">Головна</a>        
        
         <a class="nav__link" href="Cont.php">Зворотній зв'язок</a>
        <a class="nav__link" href="http://localhost:8050">Прогнозування акцій</a>
               
    </div>
    <div class="container">
        <div class="registration-form">
            <h2>Створити обліковий запис</h2>
            <form action="reg1.php" method="post">
                <label for="username">нік:</label>
                <input type="text" id="username" name="username" required><br><br>
                <label for="email">Електорона адреса:</label>
                <input type="email" id="email" name="email" required><br><br>
                <label for="password">Пароль:</label>
                <input type="password" id="pass" name="pass" required><br><br>
                <button type="submit">Зараєструватись</button>
            </form>
        </div>
    </div>
</body>
</html>