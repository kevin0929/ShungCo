function previewCSV() {
    const csvFileInput = document.getElementById('csvFileInput');
    const csvPreview = document.querySelector('.csv-preview');

    if (csvFileInput.files.length > 0) {
        const file = csvFileInput.files[0];
        const reader = new FileReader();

        reader.onload = function (e) {
            const csvContent = e.target.result;
            const lines = csvContent.split('\n');

            lines.forEach(line => {
                const columns = line.split(',');
                const studentInfo = {
                    // we will not show student name
                    name: columns[0],
                    role: columns[2],
                };

                // create text show in the preview block
                const previewElement = document.createElement('div');
                previewElement.textContent = `${studentInfo.name}, ${studentInfo.role}`;
                csvPreview.appendChild(previewElement);
            });
        };

        reader.readAsText(file);
    } else {
        alert("請選擇一個CSV檔案");
    }
}

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
    fetch("/teacher/list", {
        method: "POST",
        body: formData,
    })
        .then(response => {
            if (response.ok) {
                alert("上傳成功")
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

function logout() {
    window.location.href = "/login";
}
