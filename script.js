function sendMessage() {
    const input = document.getElementById('user-input');
    const chatBox = document.getElementById('chat-box');
    
    // Show user message
    chatBox.innerHTML += `<div class="user-message">${input.value}</div>`;
    
    fetch('/chat', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({message: input.value})
    })
    .then(response => response.json())
    .then(data => {
        chatBox.innerHTML += `<div class="bot-message">${data.message}</div>`;
        if(data.location) {
            chatBox.innerHTML += `<div class="bot-message">📍 Location: ${data.location}</div>`;
        }
        input.value = '';
        chatBox.scrollTop = chatBox.scrollHeight;
    });
}

function triggerEmergency() {
    fetch('/chat', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({message: "EMERGENCY HELP NEEDED"})
    })
    .then(response => response.json())
    .then(data => {
        alert(data.message);
    });
}