document.addEventListener("DOMContentLoaded", function () {
    const videoLinks = document.querySelectorAll(".video-link");
    const videoContainer = document.getElementById("video-container");

    videoLinks.forEach(function (link) {
        link.addEventListener("click", function (event) {
            event.preventDefault();
            const videoURL = link.getAttribute("data-url");

            const videoElement = document.createElement("video");
            videoElement.controls = true;
            const sourceElement = document.createElement("source");
            sourceElement.src = videoURL;
            sourceElement.type = "video/mp4";

            videoElement.appendChild(sourceElement);

            videoContainer.innerHTML = "";
            videoContainer.appendChild(videoElement);
        });
    });
});

function logout() {
    window.location.href = "/login";
}