function openChangePasswordModal(username) {
    var modal = document.getElementById("changePasswordModal");
    modal.style.display = "block";

    var changePasswordForm = document.getElementById("changePasswordForm");

    changePasswordForm.addEventListener("submit", function (event) {
        event.preventDefault();

        // get input
        var newPasswordInput = document.getElementById("new_password");
        var newPassword = newPasswordInput.value

        var data = {
            "change_column": "password",
            "new_data": newPassword,
            "username": username
        }

        fetch("/admin/change_personnel", {
            method: "PUT",
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

        var data = {
            "change_column": "role",
            "new_data": selectRole,
            "username": username 
        }

        fetch("/admin/change_personnel", {
            method: "PUT",
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
            method: "DELETE",
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

function logout() {
    window.location.href = "/login";
}
