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

    switch(strength) {
        case 0:
            strengthBar.style.width = "0%";
            break;
        case 1:
            strengthBar.style.width = "20%";
            break;
        case 2:
            strengthBar.style.width = "40%";
            break;
        case 3:
            strengthBar.style.width = "60%";
            break;
        case 4:
            strengthBar.style.width = "80%";
            break;
        case 5:
            strengthBar.style.width = "100%";
            break;
        case 6:
            strengthBar.style.width = "120%";
            break;
    }
});
