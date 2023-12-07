function upload() {
    var csvfile = document.getElementById('csvFileInput');
    var file = csvfile.files[0];

    if (!file) {
        alert("請選擇檔案再上傳!");
        return;
    }

    const formData = new FormData()
    formData.append("csvfile", file)

    // post to backend route 'list'
    fetch("/list", {
        method: "POST",
        body: formData,
    })
        .then(response => {
            if (response.ok) {
                alert("上傳成功");
            }
            else {
                alert("上傳失敗");
            }
        })
        .catch(error => {
            console.error("error msg : ", error);
            alert("發生錯誤，請稍後再試!");
        })
}
