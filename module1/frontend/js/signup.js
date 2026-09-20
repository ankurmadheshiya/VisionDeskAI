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

document.getElementById("signupForm").addEventListener("submit", async function(e) {
    e.preventDefault();
    
    const messageEl = document.getElementById("message");
    messageEl.className = "auth-message"; // Reset styling
    messageEl.style.display = "none";
    
    const data = {
        name: document.getElementById("name").value,
        email: document.getElementById("email").value,
        password: document.getElementById("password").value
    };
    
    try {
        const response = await fetch("http://127.0.0.1:8000/signup", {
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
            messageEl.innerText = displayMessage || "Account created successfully!";
            messageEl.style.display = "block";
            
            // Redirect to login after a short delay
            setTimeout(() => {
                window.location.href = "login.html";
            }, 1200);
        } else {
            messageEl.classList.add("error");
            messageEl.innerText = displayMessage || "Failed to create account.";
            messageEl.style.display = "block";
        }
    } catch (error) {
        messageEl.classList.add("error");
        messageEl.innerText = "Failed to connect to authentication server.";
        messageEl.style.display = "block";
    }
});