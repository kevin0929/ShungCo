function openChangePasswordModal(username) {
    var modal = document.getElementById("changePasswordModal");
    modal.style.display = "block";

    var changePasswordForm = document.getElementById("changePasswordForm");

    changePasswordForm.addEventListener("submit", function (event) {
        event.preventDefault;

        // get input
        var oldPasswordInput = document.getElementById("old_password");
        var newPasswordInput = document.getElementById("new_password");

        var oldPassword = oldPasswordInput.value
        var newPassword = newPasswordInput.value

        data = {
            "old_password": oldPassword,
            "new_password": newPassword,
            "username": username
        }

        fetch("/admin/change_password", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(data)
        })
            .then(response => {
                if (response.redirected) {
                    alert("更新成功!");
                    closeModal("changePasswordModal");

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

function openChangeRoleModal(username) {
    var modal = document.getElementById("changeRoleModal");
    modal.style.display = "block";

    var changeRoleForm = document.getElementById("changeRoleForm");

    changeRoleForm.addEventListener("submit", function (event) {
        event.preventDefault();

        var newRoleSelect = document.getElementById("new_role");
        var selectRole = newRoleSelect.value;

        var data = { "username": username, "newRole": selectRole }

        fetch("/admin/change_role", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(data)
        })
            .then(response => {
                if (response.redirected) {
                    alert("更改成功!");
                    closeModal("changeRoleModal");

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

function openDeleteUserModal(username) {
    var modal = document.getElementById("deleteUserModal");
    modal.style.display = "block";

    var deleteUserForm = document.getElementById("deleteUserForm")

    deleteUserForm.addEventListener("submit", function (event) {
        event.preventDefault();

        var data = { "username": username }

        fetch("/admin/delete_user", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(data)
        })
            .then(response => {
                if (response.redirected) {
                    alert("刪除成功");
                    closeModal("deleteUserModal");

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

function closeModal(modalId) {
    var modal = document.getElementById(modalId);
    modal.style.display = "none";
}

// 假設有一個 logout 函數
function logout() {
    window.location.href = "/login";
}