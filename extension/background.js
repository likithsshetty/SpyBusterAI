chrome.tabs.onUpdated.addListener((tabId, changeInfo, tab) => {
    if (changeInfo.status === "complete" && tab.url) {
        checkWebsiteSafety(tabId, tab.url);
    }
});

function checkWebsiteSafety(tabId, url) {
    fetch("http://127.0.0.1:5000/api/v1/", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ url: url })
    })
    .then(response => response.json())
    .then(data => {
        if (data.status === "Unsafe") {
            chrome.tabs.update(tabId, { url: "warning.html" });  // Redirect to warning page
        }
        else {
            document.getElementById("status").textContent = data.status;
            document.getElementById("message").textContent = data.message;
        }
    })
    .catch(error => console.error("Error checking website:", error));
}
