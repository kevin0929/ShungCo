function summit() {
    var username = document.getElementById("username").value;
    var password = document.getElementById("password").value;

    console.log(username)
    console.log(password)

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
                response.json().then(data => {
                    alert(data.msg);
                })
            }
        })
        .catch(error => {
            console.error("error.")
        })
}