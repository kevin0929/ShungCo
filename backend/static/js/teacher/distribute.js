window.onload = function () {
    var distributeVideoForm = document.getElementById("video-assignment-form");

    distributeVideoForm.addEventListener("submit", function (event) {
        event.preventDefault();

        var student_select = document.getElementById("student-select");
        var video_select = document.getElementById("video-select");

        var data = {
            "student_name": student_select.value,
            "video_title": video_select.value
        }

        console.log(data);

        fetch("/teacher/distribute_video", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(data)
        })
            .then(response => {
                if (response.redirected) {
                    alert("分配成功");

                    // refresh page
                    window.location.href = response.url;
                    return;
                }
                else {
                    alert("分配失敗");
                    response.json().then(data => {
                        console.error(data.msg);
                    })
                }
            })
            .catch(error => {
                console.error(error);
            })
    })
}

function logout() {
    window.location.href = "/login";
}