<!DOCTYPE html>
<html lang="uk">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Головна сторінка</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Kaushan+Script&family=Montserrat:wght@100&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="style5.css">
</head>
<body>
    <header class="header header--fixed">
        <div class="container">
            <div class="header__inner">
                <div class="header__logo">shares plus</div>
                <div class="center-container"></div>
                <div class="right-container">
                    <nav class="nav">
                        <a class="nav__link" href="intro.php">Головна</a>
                        
                        <a class="nav__link" href="Cont.php">Зворотній зв'язок</a>
                        <a class="nav__link" href="http://localhost:8050">Прогнозування акцій</a>
                        <?php
                            if (isset($_SESSION['userID'])) {
                                echo '<a class="login-button" href="logout.php">Вийти</a>';
                            } else {
                                echo '<a class="login-button" href="log.php">Увійти</a>';
                            }
                            echo '<a class="reg-button" href="reg.html">Зараєструватись</a>';
                        ?>
                    </nav>
                </div>
            </div>
        </div>
    </header>
    <br><br><br>
    <div class="container2">
        <section class="hero">
            <div class="hero__content">
                <h1 class="hero__title">Вітаємо на нашому сайті</h1>
                <p class="hero__subtitle">Місце для найкращих прогнозів акцій</p>
                <a href="http://localhost:8050" class="hero__button">Дізнатись більше</a>
            </div>
        </div>
        <section class="how-it-works">
    <div class="how-it-works__content">
        <h2 class="how-it-works__title">Короткий відео ролик роботи додатку</h2>
        <div class="how-it-works__video">
            <video controls>
                <source src="img/1.mp4" type="video/mp4">
                Ваш браузер не підтримує відео тег.
            </video>
        </div>
        
    </div>
</section>
<section class="features">
    <div class="features__item feedback">
        <h2 class="features__title">Зворотній зв'язок</h2>
        <p class="features__description">Залишайте свої коментарі та пропозиції.</p>
        <a href="Cont.php" class="features__button">Залишити відгук</a>
    </div>
</section>
   
</body>
</html>

