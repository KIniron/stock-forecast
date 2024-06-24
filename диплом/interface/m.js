function sendMail(event){
    event.preventDefault();
    let params = {
        name : document.getElementById("name").value,
        email :  document.getElementById("email").value,
        subject :  document.getElementById("subject").value,
        message :  document.getElementById("message").value,
    }
    emailjs.send("service_l43fssh", "template_f2vb81a", params)
    .then(function(response) {
        alert("Повідомлення відправлено!");
    }, function(error) {
        alert("Виникла помилка при відправці повідомлення: " + JSON.stringify(error));
    });
}
