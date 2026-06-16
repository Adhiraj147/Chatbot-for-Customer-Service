document.addEventListener("DOMContentLoaded", () => {
    const chatBody = document.getElementById("chat-body");
    const userInput = document.getElementById("user-input");
    const sendBtn = document.getElementById("send-btn");
    const themeToggle = document.getElementById("theme-toggle");
    const clearChatBtn = document.getElementById("clear-chat");
    const sessionId = document.getElementById("session-id").value;
    const welcomeTime = document.getElementById("welcome-time");
    
    // Set welcome message timestamp
    const now = new Date();
    if(welcomeTime) welcomeTime.innerText = now.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });

    // Auto-scroll
    const scrollToBottom = () => {
        chatBody.scrollTop = chatBody.scrollHeight;
    };

    // Dark Mode Toggle
    if (themeToggle) {
        themeToggle.addEventListener("click", () => {
            const currentTheme = document.body.getAttribute("data-theme");
            const newTheme = currentTheme === "dark" ? "light" : "dark";
            document.body.setAttribute("data-theme", newTheme);
            themeToggle.innerHTML = newTheme === "dark" ? '<i class="fa-solid fa-sun"></i>' : '<i class="fa-solid fa-moon"></i>';
        });
    }

    // Clear Chat
    if (clearChatBtn) {
        clearChatBtn.addEventListener("click", async () => {
            if (confirm("Are you sure you want to clear the chat history?")) {
                try {
                    const formData = new FormData();
                    formData.append("session_id", sessionId);
                    
                    await fetch("/clear_history", {
                        method: "POST",
                        body: formData
                    });
                    
                    // Clear UI (keep only welcome message)
                    const firstMsg = chatBody.firstElementChild;
                    chatBody.innerHTML = "";
                    chatBody.appendChild(firstMsg);
                    
                } catch (err) {
                    console.error("Error clearing history:", err);
                }
            }
        });
    }

    // Add message to UI
    const addMessage = (text, isUser = false) => {
        const msgDiv = document.createElement("div");
        msgDiv.className = `message ${isUser ? 'user-message' : 'bot-message'}`;
        
        const avatarDiv = document.createElement("div");
        avatarDiv.className = "avatar";
        avatarDiv.innerHTML = isUser ? '<i class="fa-solid fa-user"></i>' : '<i class="fa-solid fa-robot"></i>';
        
        const contentDiv = document.createElement("div");
        contentDiv.className = "content";
        
        const p = document.createElement("p");
        p.textContent = text;
        
        const timeSpan = document.createElement("span");
        timeSpan.className = "timestamp";
        timeSpan.innerText = new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
        
        contentDiv.appendChild(p);
        contentDiv.appendChild(timeSpan);
        
        msgDiv.appendChild(avatarDiv);
        msgDiv.appendChild(contentDiv);
        
        chatBody.appendChild(msgDiv);
        scrollToBottom();
    };

    // Show typing animation
    const showTyping = () => {
        const typingDiv = document.createElement("div");
        typingDiv.className = "message bot-message typing-indicator-container";
        typingDiv.id = "typing-indicator";
        
        const avatarDiv = document.createElement("div");
        avatarDiv.className = "avatar";
        avatarDiv.innerHTML = '<i class="fa-solid fa-robot"></i>';
        
        const contentDiv = document.createElement("div");
        contentDiv.className = "content";
        
        const indicator = document.createElement("div");
        indicator.className = "typing-indicator";
        indicator.innerHTML = '<div class="dot"></div><div class="dot"></div><div class="dot"></div>';
        
        contentDiv.appendChild(indicator);
        typingDiv.appendChild(avatarDiv);
        typingDiv.appendChild(contentDiv);
        
        chatBody.appendChild(typingDiv);
        scrollToBottom();
    };

    // Remove typing animation
    const removeTyping = () => {
        const indicator = document.getElementById("typing-indicator");
        if (indicator) {
            indicator.remove();
        }
    };

    // Send Message
    const sendMessage = async (text) => {
        if (!text.trim()) return;
        
        addMessage(text, true);
        userInput.value = "";
        
        showTyping();
        
        try {
            const response = await fetch("/chat", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({
                    message: text,
                    session_id: sessionId
                })
            });
            
            const data = await response.json();
            removeTyping();
            
            if (response.ok) {
                addMessage(data.response, false);
            } else {
                addMessage("Oops! Something went wrong. Please try again.", false);
            }
        } catch (error) {
            console.error("Error sending message:", error);
            removeTyping();
            addMessage("Network error. Please check your connection.", false);
        }
    };

    // Event Listeners for sending
    if (sendBtn) {
        sendBtn.addEventListener("click", () => sendMessage(userInput.value));
    }
    
    if (userInput) {
        userInput.addEventListener("keypress", (e) => {
            if (e.key === "Enter") {
                sendMessage(userInput.value);
            }
        });
    }

    // Quick Replies
    document.querySelectorAll(".qr-btn").forEach(btn => {
        btn.addEventListener("click", () => {
            const query = btn.getAttribute("data-query");
            sendMessage(query);
        });
    });
});
