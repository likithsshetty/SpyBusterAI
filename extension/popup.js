document.addEventListener("DOMContentLoaded", function () {

    chrome.tabs.query({ active: true, currentWindow: true }, (tabs) => {
        let currentUrl = tabs[0].url;
        document.getElementById("url").textContent = currentUrl;

        // Send URL to Flask API for analysis
        fetch("http://127.0.0.1:5000/api/v1/", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ url: currentUrl })
        })
        .then(response => response.json())
        .then(data => {
            document.getElementById("status").textContent = data.status;
            document.getElementById("message").textContent = data.message;

        })
        .catch(error => {
            document.getElementById("status").textContent = "Error connecting to server";
        });
    });

    document.getElementById("scanButton").addEventListener("click", () => {
        location.reload();
    });
});
