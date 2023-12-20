function uploadVideo() {
    const uploadForm = document.getElementById("upload-form");

    uploadForm.addEventListener("submit", async (e) => {
        e.preventDefault();

        const formData = new FormData(uploadForm);

        try {
            const response = await fetch("/teacher/upload_video", {
                method: "POST",
                body: formData
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