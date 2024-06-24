<!DOCTYPE html>
<html lang="uk">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Зворотній зв'язок</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Kaushan+Script&family=Montserrat:wght@100&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="style4.css">
    <script type="text/javascript" src="https://cdn.jsdelivr.net/npm/@emailjs/browser@4/dist/email.min.js"></script>
    <script type="text/javascript">
        (function(){
            emailjs.init("hic1a5X_FziM2SUX5"); 
        })();

        function sendMail(event) {
            event.preventDefault(); 
            let params = {
                name: document.getElementById("name").value,
                email: document.getElementById("email").value,
                subject: document.getElementById("subject").value,
                message: document.getElementById("message").value
            };

            emailjs.send("service_l43fssh", "template_f2vb81a", params)
                .then(function(response) {
                    alert("Повідомлення відправлено!");
                }, function(error) {
                    alert("Виникла помилка при відправці повідомлення: " + JSON.stringify(error));
                });
        }
    </script>
</head>
<body>
    <header class="header header--fixed">
        <div class="container">
            <div class="header__inner">
                <div class="header__logo">Shares plus</div>
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
                        echo '<a class="reg-button" href="reg.php">Зараєструватись</a>';
                    ?>
                    </nav>
                </div>
            </div>
        </div>
    </header>
    <br><br><br>
    <div class="container2">
            <div class="contact-form">
                <h2>Зворотній зв'язок</h2>
                <form onsubmit="sendMail(event)">
                    <label for="name">Ваш нік</label>
                    <input type="text" id="name" name="name" required>

                    <label for="email">Ваша електронна адреса</label>
                    <input type="email" id="email" name="email" required>

                    <label for="subject">Тема</label>
                    <input type="text" id="subject" name="subject" required> 

                    <label for="message">Ваше повідомлення</label>
                    <textarea id="message" name="message" rows="4" required></textarea>

                    <button type="submit">Відправити</button>
                </form>
            </div>
        </section>
    </div>
    <div class="container4">
        <h1 class="name3">Контакти:</h1>
        <div class="icons">
            <a class="icons" href="#">
                <div class="layer">
                    <span></span>
                    <span></span>
                    <span></span>
                    <span></span>
                    <span class="fa-brands fa-telegram"></span>
                </div>
                <div class="text">Telegram</div>
            </a>
        </div>  
        <div class="icons">
            <a class="icons" href="#">
                <div class="layer">
                    <span></span>
                    <span></span>
                    <span></span>
                    <span></span>
                    <span class="fa-brands fa-facebook"></span>
                </div>
                <div class="text">Facebook</div>
            </a>
        </div>  
        <div class="icons">
            <a class="icons" href="#">
                <div class="layer">
                    <span></span>
                    <span></span>
                    <span></span>
                    <span></span>
                    <span class="fa-brands fa-instagram"></span>
                </div>
                <div class="text">Instagram</div>
            </a>
        </div>  
    </div>
</body>
</html>
