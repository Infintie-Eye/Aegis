// AI Chatbot Integration Module
// Connects aichatbot.html with backend API

const API_BASE_URL = 'http://localhost:5000/api';

class AIChatbot {
    constructor() {
        this.userId = null;
        this.sessionContext = {};
        this.isProcessing = false;
        this.init();
    }

    init() {
        // Get user ID from Firebase auth or local storage
        this.userId = this.getUserId();

        // Initialize event listeners
        this.setupEventListeners();

        // Load chat history if available
        this.loadChatHistory();
    }

    getUserId() {
        // Try to get from localStorage first
        let userId = localStorage.getItem('aegis_user_id');

        if (!userId) {
            // Generate a temporary user ID
            userId = `user_${Date.now()}_${Math.random().toString(36).substring(7)}`;
            localStorage.setItem('aegis_user_id', userId);
        }

        return userId;
    }

    setupEventListeners() {
        const sendBtn = document.getElementById('sendBtn');
        const chatInput = document.getElementById('chatInput');

        if (sendBtn) {
            sendBtn.addEventListener('click', () => this.sendMessage());
        }

        if (chatInput) {
            chatInput.addEventListener('keypress', (e) => {
                if (e.key === 'Enter' && !e.shiftKey) {
                    e.preventDefault();
                    this.sendMessage();
                }
            });
        }
    }

    async sendMessage() {
        const chatInput = document.getElementById('chatInput');
        const message = chatInput.value.trim();

        if (!message || this.isProcessing) return;

        // Clear input
        chatInput.value = '';

        // Add user message to chat
        this.addMessageToUI(message, true);

        // Show typing indicator
        this.showTypingIndicator();

        this.isProcessing = true;

        try {
            // Send message to backend
            const response = await fetch(`${API_BASE_URL}/chat/message`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    message: message,
                    user_id: this.userId,
                    session_context: this.sessionContext
                })
            });

            const data = await response.json();

            // Remove typing indicator
            this.removeTypingIndicator();

            if (data.status === 'success') {
                // Add AI response to chat
                this.addMessageToUI(data.response, false);

                // Display wellness suggestions if available
                if (data.wellness_suggestions && data.wellness_suggestions.length > 0) {
                    this.displayWellnessSuggestions(data.wellness_suggestions);
                }

                // Display community suggestions if available
                if (data.community_suggestions && Object.keys(data.community_suggestions).length > 0) {
                    this.displayCommunitySuggestions(data.community_suggestions);
                }

                // Check safety status
                if (data.safety_status && data.safety_status.crisis_level >= 7) {
                    this.handleCrisisAlert(data.safety_status);
                }
            } else {
                // Show fallback response
                this.addMessageToUI(
                    data.fallback_response || "I'm here to listen. Could you tell me more?",
                    false
                );
            }

        } catch (error) {
            console.error('Error sending message:', error);
            this.removeTypingIndicator();
            this.addMessageToUI(
                "I'm having trouble connecting right now. Please try again in a moment.",
                false
            );
        } finally {
            this.isProcessing = false;
        }
    }

    addMessageToUI(message, isUser) {
        const chatMessages = document.getElementById('chatMessages');
        if (!chatMessages) return;

        const messageDiv = document.createElement('div');
        messageDiv.classList.add('message');
        messageDiv.classList.add(isUser ? 'user-message' : 'ai-message');

        const messageText = document.createElement('div');
        messageText.textContent = message;

        const messageTime = document.createElement('div');
        messageTime.classList.add('message-time');
        messageTime.textContent = this.getCurrentTime();

        messageDiv.appendChild(messageText);
        messageDiv.appendChild(messageTime);

        chatMessages.appendChild(messageDiv);
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }

    showTypingIndicator() {
        const chatMessages = document.getElementById('chatMessages');
        if (!chatMessages) return;

        const typingDiv = document.createElement('div');
        typingDiv.classList.add('typing-indicator');
        typingDiv.id = 'typingIndicator';

        for (let i = 0; i < 3; i++) {
            const span = document.createElement('span');
            typingDiv.appendChild(span);
        }

        chatMessages.appendChild(typingDiv);
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }

    removeTypingIndicator() {
        const typingIndicator = document.getElementById('typingIndicator');
        if (typingIndicator) {
            typingIndicator.remove();
        }
    }

    getCurrentTime() {
        const now = new Date();
        return now.toLocaleTimeString([], {hour: '2-digit', minute: '2-digit'});
    }

    displayWellnessSuggestions(suggestions) {
        // Create a wellness suggestions panel
        const chatMessages = document.getElementById('chatMessages');
        if (!chatMessages) return;

        const suggestionsDiv = document.createElement('div');
        suggestionsDiv.classList.add('message', 'ai-message', 'wellness-suggestions');

        let suggestionsHTML = '<div class="suggestions-header">💡 Wellness Suggestions</div><ul>';

        suggestions.slice(0, 3).forEach(suggestion => {
            if (typeof suggestion === 'string') {
                suggestionsHTML += `<li>${suggestion}</li>`;
            } else if (suggestion.title) {
                suggestionsHTML += `<li><strong>${suggestion.title}</strong>: ${suggestion.description}</li>`;
            }
        });

        suggestionsHTML += '</ul>';
        suggestionsDiv.innerHTML = suggestionsHTML;

        chatMessages.appendChild(suggestionsDiv);
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }

    displayCommunitySuggestions(communitySuggestions) {
        const chatMessages = document.getElementById('chatMessages');
        if (!chatMessages) return;

        const communityDiv = document.createElement('div');
        communityDiv.classList.add('message', 'ai-message', 'community-suggestions');

        let communityHTML = '<div class="suggestions-header">👥 Community Support</div>';

        if (communitySuggestions.support_groups && communitySuggestions.support_groups.length > 0) {
            communityHTML += '<p>You might find these support groups helpful:</p><ul>';
            communitySuggestions.support_groups.slice(0, 2).forEach(group => {
                communityHTML += `<li>${group.name || group}</li>`;
            });
            communityHTML += '</ul>';
        }

        communityDiv.innerHTML = communityHTML;
        chatMessages.appendChild(communityDiv);
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }

    handleCrisisAlert(safetyStatus) {
        // Display crisis resources
        const chatMessages = document.getElementById('chatMessages');
        if (!chatMessages) return;

        const crisisDiv = document.createElement('div');
        crisisDiv.classList.add('message', 'ai-message', 'crisis-alert');

        crisisDiv.innerHTML = `
            <div class="crisis-header">⚠️ Immediate Support Resources</div>
            <p>If you're in crisis or considering self-harm, please reach out for immediate help:</p>
            <ul>
                <li><strong>National Suicide Prevention Lifeline:</strong> Call or text 988</li>
                <li><strong>Crisis Text Line:</strong> Text HOME to 741741</li>
                <li><strong>Emergency Services:</strong> Call 911</li>
            </ul>
            <p>You're not alone. Help is available 24/7.</p>
        `;

        chatMessages.appendChild(crisisDiv);
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }

    async loadChatHistory() {
        try {
            const response = await fetch(`${API_BASE_URL}/chat/history/${this.userId}`);
            const data = await response.json();

            if (data.status === 'success' && data.history && data.history.length > 0) {
                // Display recent messages
                data.history.slice(-10).forEach(msg => {
                    if (msg.role === 'user') {
                        this.addMessageToUI(msg.content, true);
                    } else if (msg.role === 'assistant') {
                        this.addMessageToUI(msg.content, false);
                    }
                });
            }
        } catch (error) {
            console.error('Error loading chat history:', error);
        }
    }

    async getInsights() {
        try {
            const response = await fetch(`${API_BASE_URL}/chat/insights/${this.userId}`);
            const data = await response.json();

            if (data.status === 'success') {
                return data.insights;
            }
        } catch (error) {
            console.error('Error fetching insights:', error);
        }
        return null;
    }

    async clearHistory() {
        try {
            const response = await fetch(`${API_BASE_URL}/chat/clear/${this.userId}`, {
                method: 'DELETE'
            });
            const data = await response.json();

            if (data.status === 'success') {
                // Clear UI
                const chatMessages = document.getElementById('chatMessages');
                if (chatMessages) {
                    chatMessages.innerHTML = `
                        <div class="message ai-message">
                            Hello! I'm your AI companion. How can I help you today?
                            <div class="message-time">Just now</div>
                        </div>
                    `;
                }
            }
        } catch (error) {
            console.error('Error clearing history:', error);
        }
    }
}

// Initialize chatbot when DOM is loaded
let aiChatbot;

document.addEventListener('DOMContentLoaded', () => {
    aiChatbot = new AIChatbot();
});

// Export for use in other modules
if (typeof module !== 'undefined' && module.exports) {
    module.exports = AIChatbot;
}
