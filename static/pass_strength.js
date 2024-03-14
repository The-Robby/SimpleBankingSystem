document.getElementById("password").addEventListener("input", function() {
    var password = document.getElementById("password").value;
    var strengthBar = document.getElementById("strength");
    var strength = 0;

    if (password.match(/(?=.*[a-z])/)) {
        strength += 1;
    }
    if (password.match(/(?=.*\d)/)) {
        strength += 1;
    }
    if (password.match(/(?=.*[A-Z])/)) {
        strength += 1;
    }
    if (password.match(/(?=.*[\W_])/)) {
        strength += 1;
    }
    if (password.length >= 6) {
        strength += 1;
    }

    var width = strength * 20;

    strengthBar.style.transition = "width 0.3s ease";
    strengthBar.style.width = width + "%";

});
