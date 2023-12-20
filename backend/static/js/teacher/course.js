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
            "change_column": "course_title",
            "new_data": newTitle,
            "course_id": id
        }

        fetch("/teacher/change_course", {
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

function openModifyTeacherModal(id) {
    var modal = document.getElementById("modifyTeacherModal");
    modal.style.display = "block";

    var modifyTeacherForm = document.getElementById("modifyTeacherForm");

    modifyTeacherForm.addEventListener("submit", function (event) {
        event.preventDefault();

        var newTeacherInput = document.getElementById("new_teacher");
        var newTeacher = newTeacherInput.value;

        var data = {
            "change_column": "teacher_name",
            "new_data": newTeacher,
            "course_id": id
        }

        fetch("/teacher/change_course", {
            method: "PUT",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(data)
        })
            .then(response => {
                if (response.redirected) {
                    alert("更改成功!");
                    closeModal("modifyTitleModal");

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

function openModifyDescribeModal(id) {
    var modal = document.getElementById("modifyDescribeModal");
    modal.style.display = "block";

    var modifyDescribeForm = document.getElementById("modifyDescribeForm");

    modifyDescribeForm.addEventListener("submit", function (event) {
        event.preventDefault();

        var newDescribeInput = document.getElementById("new_describe");
        var newDescribe = newDescribeInput.value;

        var data = {
            "change_column": "course_describe",
            "new_data": newDescribe,
            "course_id": id
        }

        fetch("/teacher/change_course", {
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

function openDeleteCourseModal(id) {
    var modal = document.getElementById("deleteCourseModal");
    modal.style.display = "block";

    var deleteCourseForm = document.getElementById("deleteCourseForm")

    deleteCourseForm.addEventListener("submit", function (event) {
        event.preventDefault();

        var data = { "course_id": id }

        fetch("/teacher/delete_course", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(data)
        })
            .then(response => {
                if (response.redirected) {
                    alert("刪除成功");
                    closeModal("deleteCourseModal");

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

function uploadCourse() {
    var addCourseForm = document.getElementById("add-course-form");

    addCourseForm.addEventListener("submit", function (event) {
        event.preventDefault()

        // get value we want to upload
        var courseTitleInput = document.getElementById("course-title");
        var courseTeacherInput = document.getElementById("course-teacher");
        var courseDescribeInput = document.getElementById("course-description");

        var courseTitle = courseTitleInput.value;
        var courseTeacher = courseTeacherInput.value;
        var courseDescribe = courseDescribeInput.value;

        var data = {
            "course_title": courseTitle,
            "course_teacher": courseTeacher,
            "course_describe": courseDescribe
        }

        fetch("/teacher/upload_course", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(data)
        })
            .then(response => {
                if (response.redirected) {
                    alert("上傳成功!");

                    window.location.href = response.url;
                    return;
                }
                else {
                    alert("上傳失敗!");
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

function closeModal(modalId) {
    var modal = document.getElementById(modalId);
    modal.style.display = "none";
}

function logout() {
    window.location.href = "/login";
}
