function openModifyTitleModal(id) {
    var modal = document.getElementById("modifyTitleModal");
    modal.style.display = "block";

    var modifyTitleForm = document.getElementById("modifyTitleForm");

    modifyTitleForm.addEventListener("submit", function (event) {
        event.preventDefault();

        // get input
        var newTitleInput = document.getElementById("new_title");
        var newTitle = newTitleInput.value

        var data = {
            "change_column": "video_title",
            "new_data": newTitle,
            "video_id": id
        }

        fetch("/teacher/change_video", {
            method: "PUT",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(data)
        })
            .then(response => {
                if (response.redirected) {
                    alert("更新成功!");
                    closeModal("modifyTitleModal");

                    window.location.href = response.url;
                    return;
                }
                else {
                    alert("更新失敗");
                    response.json().then(data => {
                        console.error(data.msg);
                    })
                }
            })
            .catch(error => {
                console.error("The Error : ", error);
            })
    })
}

function openModifyDescribeModal(id) {
    var modal = document.getElementById("modifyDescribeModal");
    modal.style.display = "block";

    var modifyDescribeForm = document.getElementById("modifyDescribeForm");

    modifyDescribeForm.addEventListener("submit", function (event) {
        event.preventDefault();

        var newDescribeInput = document.getElementById("new_describe");
        var newDescribe = newDescribeInput.value;

        var data = {
            "change_column": "video_describe",
            "new_data": newDescribe,
            "video_id": id
        }

        fetch("/teacher/change_video", {
            method: "PUT",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(data)
        })
            .then(response => {
                if (response.redirected) {
                    alert("更改成功!");
                    closeModal("modifyDescribeModal");

                    // refresh manage page
                    window.location.href = response.url;
                    return;
                }
                else {
                    alert("更新失敗");
                    response.json().then(data => {
                        console.error(data.msg);
                    })
                }
            })
            .catch(error => {
                console.error("Error : ", error);
            })
    })
}

function openDeleteVideoModal(id) {
    var modal = document.getElementById("deleteVideoModal");
    modal.style.display = "block";

    var deleteVideoForm = document.getElementById("deleteVideoForm")

    deleteVideoForm.addEventListener("submit", function (event) {
        event.preventDefault();

        var data = { "video_id": id }

        fetch("/teacher/delete_video", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(data)
        })
            .then(response => {
                if (response.redirected) {
                    alert("刪除成功");
                    closeModal("deleteVideoModal");

                    // refresh page
                    window.location.href = response.url;
                    return;
                }
                else {
                    alert("刪除失敗");
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

function uploadVideo() {
    const uploadForm = document.getElementById("upload-form");

    uploadForm.addEventListener("submit", async (e) => {
        e.preventDefault();

        // get input
        var videoTitleInput = document.getElementById("video-title");
        var videoDescribeInput = document.getElementById("video-description");
        var videoCourseIdInput = document.getElementById("course-id");

        var videoTitle = videoTitleInput.value;
        var videoDescribe = videoDescribeInput.value;
        var videoCourseId = videoCourseIdInput.value;

        const formData = new FormData(uploadForm);

        // make json
        const data = {
            "video_title": videoTitle,
            "video_describe": videoDescribe,
            "course_id": videoCourseId,
        };

        formData.append("data", JSON.stringify(data));

        try {
            const response = await fetch("/teacher/upload_video", {
                method: "POST",
                body: formData,
            });

            if (response.redirected) {
                alert("上傳成功!");

                window.location.href = response.url;
                return;
            }
            else {
                alert("上傳失敗!");
            }
        }
        catch (error) {
            console.error("The error : ", error);
        }
    });
}

function closeModal(modalId) {
    var modal = document.getElementById(modalId);
    modal.style.display = "none";
}

function logout() {
    window.location.href = "/login";
}