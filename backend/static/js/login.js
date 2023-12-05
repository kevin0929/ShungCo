function summit() {
    var username = document.getElementById("username").value;
    var password = document.getElementById("password").value;
    var data = { "username": username, "password": password };

    fetch("/verify", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify(data)
    })
        .then(response => {
            if (response.redirected) {
                window.location.href = response.url;
                return;
            }
            else {
                console.log("Password is wrong.");
                alert("Get out bitch!");
            }
        })
        .catch(error => {
            console.error("error.")
        })
}