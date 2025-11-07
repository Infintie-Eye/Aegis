// Firebase Chat Module for Real-time Chat
import { db, auth } from './firebase.js';
import { 
    collection, 
    addDoc, 
    query, 
    orderBy, 
    onSnapshot, 
    serverTimestamp,
    limit,
    where,
    getDocs,
    updateDoc,
    doc,
    getDoc,
    setDoc
} from 'https://www.gstatic.com/firebasejs/11.0.0/firebase-firestore.js';
import { onAuthStateChanged } from 'https://www.gstatic.com/firebasejs/11.0.0/firebase-auth.js';

class FirebaseChat {
    constructor(roomId, chatMessagesContainer, messageInput, sendButton) {
        this.roomId = roomId;
        this.chatMessagesContainer = chatMessagesContainer;
        this.messageInput = messageInput;
        this.sendButton = sendButton;
        this.currentUser = null;
        this.unsubscribe = null;
        this.userDisplayName = null;
        this.userInitials = null;
        
        this.init();
    }

    async init() {
        // Wait for auth state
        onAuthStateChanged(auth, async (user) => {
            if (user) {
                this.currentUser = user;
                await this.setupUserProfile();
                this.setupEventListeners();
                this.loadMessages();
            } else {
                console.error('User not authenticated');
            }
        });
    }

    async setupUserProfile() {
        if (!this.currentUser) return;
        
        // Get or create user profile
        const userRef = doc(db, 'users', this.currentUser.uid);
        const userSnap = await getDoc(userRef);
        
        if (userSnap.exists()) {
            const userData = userSnap.data();
            this.userDisplayName = userData.displayName || this.generateAnonymousName();
            this.userInitials = userData.initials || this.getInitials(this.userDisplayName);
        } else {
            // Create a profile appropriate to the auth state.
            const isAnon = !!this.currentUser.isAnonymous;
            if (isAnon) {
                this.userDisplayName = this.generateAnonymousName();
            } else {
                // Prefer the provider displayName, then email local part, then fallback anonymous name
                this.userDisplayName = this.currentUser.displayName || (this.currentUser.email ? this.currentUser.email.split('@')[0] : this.generateAnonymousName());
            }
            this.userInitials = this.getInitials(this.userDisplayName);

            await setDoc(userRef, {
                email: this.currentUser.email || null,
                displayName: this.userDisplayName,
                initials: this.userInitials,
                createdAt: serverTimestamp(),
                isAnonymous: isAnon
            });
        }
    }

    generateAnonymousName() {
        const adjectives = ['Anonymous', 'Silent', 'Hopeful', 'Peaceful', 'Kind', 'Gentle', 'Brave', 'Calm', 'Serene', 'Quiet'];
        const nouns = ['Soul', 'Heart', 'Spirit', 'Mind', 'Voice', 'Light', 'Star', 'Moon', 'Cloud', 'River', 'Wave', 'Dream'];
        const adjective = adjectives[Math.floor(Math.random() * adjectives.length)];
        const noun = nouns[Math.floor(Math.random() * nouns.length)];
        return `${adjective} ${noun}`;
    }

    getInitials(name) {
        const parts = name.split(' ');
        if (parts.length >= 2) {
            return (parts[0][0] + parts[1][0]).toUpperCase();
        }
        return name.substring(0, 2).toUpperCase();
    }

    setupEventListeners() {
        // Send button click
        this.sendButton.addEventListener('click', () => this.sendMessage());
        
        // Enter key press
        this.messageInput.addEventListener('keypress', (e) => {
            if (e.key === 'Enter' && !e.shiftKey) {
                e.preventDefault();
                this.sendMessage();
            }
        });
    }

    async sendMessage() {
        const messageText = this.messageInput.value.trim();
        
        if (!messageText || !this.currentUser) return;
        
        try {
            await addDoc(collection(db, 'chatrooms', this.roomId, 'messages'), {
                text: messageText,
                userId: this.currentUser.uid,
                displayName: this.userDisplayName,
                initials: this.userInitials,
                timestamp: serverTimestamp(),
                createdAt: new Date().toISOString()
            });
            
            // Clear input
            this.messageInput.value = '';
            
            // Update user's last activity
            const userRef = doc(db, 'users', this.currentUser.uid);
            await updateDoc(userRef, {
                lastActivity: serverTimestamp()
            });
            
        } catch (error) {
            console.error('Error sending message:', error);
            alert('Failed to send message. Please try again.');
        }
    }

    loadMessages() {
        const messagesRef = collection(db, 'chatrooms', this.roomId, 'messages');
        const q = query(messagesRef, orderBy('timestamp', 'asc'));
        
        // Clear existing messages
        this.chatMessagesContainer.innerHTML = '';
        
        // Listen for real-time updates
        this.unsubscribe = onSnapshot(q, (snapshot) => {
            snapshot.docChanges().forEach((change) => {
                if (change.type === 'added') {
                    this.displayMessage(change.doc.data(), change.doc.id);
                }
            });
            
            // Scroll to bottom
            setTimeout(() => {
                this.chatMessagesContainer.scrollTop = this.chatMessagesContainer.scrollHeight;
            }, 100);
        }, (error) => {
            console.error('Error loading messages:', error);
        });
    }

    displayMessage(messageData, messageId) {
        const isOwn = this.currentUser && messageData.userId === this.currentUser.uid;
        
        const messageElement = document.createElement('div');
        messageElement.classList.add('message');
        if (isOwn) {
            messageElement.classList.add('own');
        }
        messageElement.dataset.messageId = messageId;
        
        // Format timestamp
        let timeString = 'Just now';
        if (messageData.timestamp) {
            const timestamp = messageData.timestamp.toDate ? messageData.timestamp.toDate() : new Date(messageData.createdAt);
            timeString = timestamp.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
        }
        
        messageElement.innerHTML = `
            <div class="message-avatar">${messageData.initials || 'AN'}</div>
            <div class="message-content">
                <div class="message-header">
                    <div class="message-author">${isOwn ? 'You' : (messageData.displayName || 'Anonymous')}</div>
                    <div class="message-time">${timeString}</div>
                </div>
                <div class="message-text">${this.escapeHtml(messageData.text)}</div>
            </div>
        `;
        
        this.chatMessagesContainer.appendChild(messageElement);
        
        // Scroll to bottom
        this.chatMessagesContainer.scrollTop = this.chatMessagesContainer.scrollHeight;
    }

    escapeHtml(text) {
        const div = document.createElement('div');
        div.textContent = text;
        return div.innerHTML;
    }

    cleanup() {
        if (this.unsubscribe) {
            this.unsubscribe();
        }
    }
}

// Export for use in pages
export default FirebaseChat;

