async function checkDatabase() {
    const dot = document.getElementById("db-status-dot");
    const text = document.getElementById("db-status-text");
    
    try {
        const response = await fetch("http://127.0.0.1:8000/db-check");
        const result = await response.json();
        
        if (response.ok && result.status === "connected") {
            dot.className = "status-dot connected";
            text.className = "status-text connected";
            text.innerText = "Database Connected";
        } else {
            throw new Error(result.detail || "Database connection issue");
        }
    } catch (error) {
        dot.className = "status-dot disconnected";
        text.className = "status-text disconnected";
        text.innerText = "Database Disconnected";
    }
}

// Check database connection on page load
document.addEventListener("DOMContentLoaded", checkDatabase);

document.getElementById("loginForm").addEventListener("submit", async function(e) {
    e.preventDefault();
    
    const messageEl = document.getElementById("message");
    messageEl.className = "auth-message"; // Reset styling
    messageEl.style.display = "none";
    
    const data = {
        email: document.getElementById("email").value,
        password: document.getElementById("password").value
    };
    
    try {
        const response = await fetch("http://127.0.0.1:8000/login", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(data)
        });
        
        const result = await response.json();
        const displayMessage = result.message || result.detail;
        
        if (response.ok) {
            messageEl.classList.add("success");
            messageEl.innerText = displayMessage || "Login Successful!";
            messageEl.style.display = "block";
            
            // Redirect after a short delay to let the user see success message
            setTimeout(() => {
                window.location.href = "dashboard.html";
            }, 800);
        } else {
            messageEl.classList.add("error");
            messageEl.innerText = displayMessage || "Invalid Credentials.";
            messageEl.style.display = "block";
        }
    } catch (error) {
        messageEl.classList.add("error");
        messageEl.innerText = "Failed to connect to authentication server.";
        messageEl.style.display = "block";
    }
});