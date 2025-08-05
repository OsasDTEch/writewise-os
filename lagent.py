import streamlit as st
from query import app  # Compiled LangGraph app
from typing import List, Any
import time
import json

st.set_page_config(
    page_title="📝 WriteWise - Appwrite AI Assistant",
    layout="wide",
    initial_sidebar_state="collapsed",
    menu_items={
        'Get Help': 'https://appwrite.io/docs',
        'Report a bug': "https://github.com/appwrite/appwrite/issues",
        'About': "# WriteWise 🧠\nYour intelligent Appwrite documentation assistant"
    }
)

# Enhanced CSS with Appwrite-inspired branding and futuristic design
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@300;400;500;600;700&family=Inter:wght@300;400;500;600;700&display=swap');

    :root {
        --appwrite-pink: #fd366e;
        --appwrite-purple: #7c3aed;
        --appwrite-blue: #0f172a;
        --appwrite-dark: #0f0f23;
        --appwrite-gradient: linear-gradient(135deg, #fd366e 0%, #7c3aed 50%, #2563eb 100%);
        --glass-bg: rgba(255, 255, 255, 0.08);
        --glass-border: rgba(255, 255, 255, 0.12);
    }

    * {
        font-family: 'Inter', sans-serif;
    }

    .stApp {
        background: var(--appwrite-dark);
        background-image: 
            radial-gradient(circle at 20% 80%, rgba(253, 54, 110, 0.1) 0%, transparent 50%),
            radial-gradient(circle at 80% 20%, rgba(124, 58, 237, 0.1) 0%, transparent 50%),
            radial-gradient(circle at 40% 40%, rgba(37, 99, 235, 0.05) 0%, transparent 50%);
        min-height: 100vh;
        color: white;
    }

    .main-container {
        background: var(--glass-bg);
        backdrop-filter: blur(24px);
        border-radius: 24px;
        padding: 2.5rem;
        margin: 1rem;
        border: 1px solid var(--glass-border);
        box-shadow: 
            0 8px 32px rgba(0, 0, 0, 0.3),
            inset 0 1px 0 rgba(255, 255, 255, 0.1);
    }

    .brand-header {
        text-align: center;
        margin-bottom: 3rem;
        position: relative;
    }

    .logo-container {
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 1rem;
        margin-bottom: 1rem;
    }

    .logo {
        width: 60px;
        height: 60px;
        background: var(--appwrite-gradient);
        border-radius: 16px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 2rem;
        font-weight: bold;
        color: white;
        box-shadow: 0 8px 24px rgba(253, 54, 110, 0.3);
        animation: pulse 2s infinite;
    }

    @keyframes pulse {
        0%, 100% { transform: scale(1); }
        50% { transform: scale(1.05); }
    }

    .brand-name {
        font-size: 3.5rem;
        font-weight: 800;
        background: var(--appwrite-gradient);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        font-family: 'JetBrains Mono', monospace;
        letter-spacing: -2px;
    }

    .brand-tagline {
        font-size: 1.1rem;
        color: rgba(255, 255, 255, 0.7);
        font-weight: 400;
        margin-top: 0.5rem;
    }

    .appwrite-badge {
        display: inline-flex;
        align-items: center;
        gap: 0.5rem;
        background: rgba(253, 54, 110, 0.1);
        border: 1px solid rgba(253, 54, 110, 0.3);
        border-radius: 20px;
        padding: 6px 16px;
        font-size: 0.9rem;
        color: #fd366e;
        font-weight: 500;
        margin-top: 1rem;
    }

    .chat-container {
        background: rgba(0, 0, 0, 0.4);
        border-radius: 20px;
        padding: 2rem;
        margin-bottom: 2rem;
        max-height: 550px;
        overflow-y: auto;
        border: 1px solid var(--glass-border);
        position: relative;
        backdrop-filter: blur(10px);
    }

    .chat-container::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 3px;
        background: var(--appwrite-gradient);
        border-radius: 20px 20px 0 0;
    }

    .chat-container::-webkit-scrollbar {
        width: 8px;
    }

    .chat-container::-webkit-scrollbar-track {
        background: rgba(255, 255, 255, 0.05);
        border-radius: 4px;
    }

    .chat-container::-webkit-scrollbar-thumb {
        background: var(--appwrite-gradient);
        border-radius: 4px;
    }

    .message {
        margin-bottom: 1.5rem;
        animation: messageSlide 0.4s ease-out;
    }

    @keyframes messageSlide {
        from {
            opacity: 0;
            transform: translateY(30px) scale(0.95);
        }
        to {
            opacity: 1;
            transform: translateY(0) scale(1);
        }
    }

    .user-message {
        display: flex;
        justify-content: flex-end;
    }

    .user-bubble {
        background: var(--appwrite-gradient);
        color: white;
        padding: 16px 24px;
        border-radius: 24px 24px 8px 24px;
        max-width: 75%;
        font-weight: 500;
        box-shadow: 0 8px 24px rgba(253, 54, 110, 0.2);
        position: relative;
    }

    .user-bubble::before {
        content: '👤';
        position: absolute;
        top: -8px;
        right: -8px;
        background: rgba(255, 255, 255, 0.2);
        width: 24px;
        height: 24px;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 12px;
    }

    .bot-message {
        display: flex;
        justify-content: flex-start;
    }

    .bot-bubble {
        background: rgba(255, 255, 255, 0.95);
        color: #1a1a2e;
        padding: 16px 24px;
        border-radius: 24px 24px 24px 8px;
        max-width: 75%;
        font-weight: 500;
        box-shadow: 0 8px 24px rgba(0, 0, 0, 0.15);
        border-left: 4px solid var(--appwrite-pink);
        position: relative;
    }

    .bot-bubble::before {
        content: '🤖';
        position: absolute;
        top: -8px;
        left: -8px;
        background: var(--appwrite-gradient);
        width: 24px;
        height: 24px;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 12px;
    }

    .input-section {
        background: var(--glass-bg);
        backdrop-filter: blur(16px);
        border-radius: 20px;
        padding: 1.5rem;
        border: 1px solid var(--glass-border);
        position: relative;
        overflow: hidden;
    }

    .input-section::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 2px;
        background: var(--appwrite-gradient);
        border-radius: 20px 20px 0 0;
    }

    .stTextInput > div > div > input {
        background: rgba(255, 255, 255, 0.95) !important;
        border: 2px solid transparent !important;
        border-radius: 16px !important;
        color: #1a1a2e !important;
        font-weight: 500 !important;
        padding: 16px 20px !important;
        font-size: 16px !important;
        transition: all 0.3s ease !important;
    }

    .stTextInput > div > div > input:focus {
        border: 2px solid var(--appwrite-pink) !important;
        box-shadow: 0 0 0 4px rgba(253, 54, 110, 0.1) !important;
        outline: none !important;
    }

    .stButton > button {
        background: var(--appwrite-gradient) !important;
        color: white !important;
        border: none !important;
        border-radius: 16px !important;
        padding: 16px 32px !important;
        font-weight: 700 !important;
        font-size: 16px !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 8px 24px rgba(253, 54, 110, 0.3) !important;
        text-transform: uppercase !important;
        letter-spacing: 1px !important;
    }

    .stButton > button:hover {
        transform: translateY(-3px) scale(1.02) !important;
        box-shadow: 0 12px 32px rgba(253, 54, 110, 0.4) !important;
    }

    .stButton > button:active {
        transform: translateY(-1px) scale(0.98) !important;
    }

    .stats-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
        gap: 1.5rem;
        margin: 2rem 0;
    }

    .stat-card {
        background: var(--glass-bg);
        backdrop-filter: blur(16px);
        border-radius: 16px;
        padding: 1.5rem;
        border: 1px solid var(--glass-border);
        text-align: center;
        transition: all 0.3s ease;
    }

    .stat-card:hover {
        transform: translateY(-4px);
        box-shadow: 0 12px 32px rgba(253, 54, 110, 0.15);
    }

    .stat-number {
        font-size: 2.5rem;
        font-weight: 800;
        background: var(--appwrite-gradient);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-family: 'JetBrains Mono', monospace;
    }

    .stat-label {
        color: rgba(255, 255, 255, 0.8);
        font-weight: 500;
        margin-top: 0.5rem;
    }

    .typing-indicator {
        display: flex;
        align-items: center;
        gap: 12px;
        padding: 16px 24px;
        background: rgba(255, 255, 255, 0.95);
        border-radius: 24px 24px 24px 8px;
        max-width: 200px;
        box-shadow: 0 8px 24px rgba(0, 0, 0, 0.15);
        border-left: 4px solid var(--appwrite-pink);
    }

    .typing-dots {
        display: flex;
        gap: 6px;
    }

    .dot {
        width: 10px;
        height: 10px;
        border-radius: 50%;
        background: var(--appwrite-gradient);
        animation: typing 1.6s infinite;
    }

    .dot:nth-child(1) { animation-delay: 0s; }
    .dot:nth-child(2) { animation-delay: 0.3s; }
    .dot:nth-child(3) { animation-delay: 0.6s; }

    @keyframes typing {
        0%, 60%, 100% {
            transform: scale(0.8) translateY(0);
            opacity: 0.5;
        }
        30% {
            transform: scale(1.2) translateY(-12px);
            opacity: 1;
        }
    }

    .empty-state {
        text-align: center;
        padding: 4rem 2rem;
        color: rgba(255, 255, 255, 0.8);
    }

    .empty-icon {
        font-size: 5rem;
        margin-bottom: 2rem;
        background: var(--appwrite-gradient);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }

    .suggestion-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
        gap: 1rem;
        margin-top: 2rem;
    }

    .suggestion-card {
        background: var(--glass-bg);
        border: 1px solid var(--glass-border);
        border-radius: 12px;
        padding: 1rem;
        cursor: pointer;
        transition: all 0.3s ease;
        backdrop-filter: blur(8px);
    }

    .suggestion-card:hover {
        background: rgba(253, 54, 110, 0.1);
        border-color: var(--appwrite-pink);
        transform: translateY(-2px);
    }

    .clear-btn {
        position: fixed !important;
        bottom: 20px !important;
        right: 20px !important;
        z-index: 1000 !important;
        border-radius: 50% !important;
        width: 60px !important;
        height: 60px !important;
        background: rgba(220, 38, 127, 0.9) !important;
        backdrop-filter: blur(8px) !important;
    }

    .version-tag {
        position: absolute;
        top: 1rem;
        right: 1rem;
        background: rgba(124, 58, 237, 0.2);
        border: 1px solid rgba(124, 58, 237, 0.4);
        border-radius: 12px;
        padding: 4px 12px;
        font-size: 0.8rem;
        color: #a855f7;
        font-family: 'JetBrains Mono', monospace;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if "chat_history" not in st.session_state:
    st.session_state.chat_history: List[Any] = []

if "message_count" not in st.session_state:
    st.session_state.message_count = 0

if "is_processing" not in st.session_state:
    st.session_state.is_processing = False

# Main container
st.markdown('<div class="main-container">', unsafe_allow_html=True)

# Version tag
st.markdown('<div class="version-tag">v2.0 Beta</div>', unsafe_allow_html=True)

# Brand header
st.markdown("""
<div class="brand-header">
    <div class="logo-container">
        <div class="logo">W</div>
        <div>
            <div class="brand-name">WriteWise</div>
        </div>
    </div>
    <div class="brand-tagline">Your Intelligent Appwrite Documentation Assistant</div>
    <div class="appwrite-badge">
        <span>⚡</span>
        <span>Powered by Appwrite Docs</span>
    </div>
</div>
""", unsafe_allow_html=True)

# Stats section
total_messages = len(st.session_state.chat_history)
user_messages = len([msg for msg in st.session_state.chat_history if msg[0] == "You"])
bot_responses = total_messages - user_messages

st.markdown(f"""
<div class="stats-grid">
    <div class="stat-card">
        <div class="stat-number">{total_messages}</div>
        <div class="stat-label">Total Exchanges</div>
    </div>
    <div class="stat-card">
        <div class="stat-number">{user_messages}</div>
        <div class="stat-label">Questions Asked</div>
    </div>
    <div class="stat-card">
        <div class="stat-number">{bot_responses}</div>
        <div class="stat-label">Solutions Provided</div>
    </div>
</div>
""", unsafe_allow_html=True)

# Chat display
st.markdown('<div class="chat-container">', unsafe_allow_html=True)

if not st.session_state.chat_history:
    # Enhanced empty state
    st.markdown("""
    <div class="empty-state">
        <div class="empty-icon">🧠</div>
        <h2>Ready to explore Appwrite?</h2>
        <p>I'm your personal Appwrite documentation expert. Ask me anything about databases, authentication, storage, functions, and more!</p>

        <div class="suggestion-grid">
            <div class="suggestion-card">
                <h4>🗄️ Database Queries</h4>
                <p>Learn about collections, documents, and queries</p>
            </div>
            <div class="suggestion-card">
                <h4>🔐 Authentication</h4>
                <p>User management, sessions, and security</p>
            </div>
            <div class="suggestion-card">
                <h4>📁 Storage & Files</h4>
                <p>File uploads, buckets, and permissions</p>
            </div>
            <div class="suggestion-card">
                <h4>⚡ Cloud Functions</h4>
                <p>Serverless functions and deployments</p>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
else:
    # Display chat messages
    for speaker, message in st.session_state.chat_history:
        if speaker == "You":
            st.markdown(f"""
            <div class="message user-message">
                <div class="user-bubble">{message}</div>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class="message bot-message">
                <div class="bot-bubble">{message}</div>
            </div>
            """, unsafe_allow_html=True)

# Show typing indicator if processing
if st.session_state.is_processing:
    st.markdown("""
    <div class="message bot-message">
        <div class="typing-indicator">
            <span>WriteWise is thinking</span>
            <div class="typing-dots">
                <div class="dot"></div>
                <div class="dot"></div>
                <div class="dot"></div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

# Input section
st.markdown('<div class="input-section">', unsafe_allow_html=True)

with st.form("chat_form", clear_on_submit=True):
    col1, col2 = st.columns([5, 1])

    with col1:
        user_input = st.text_input(
            "Message",
            placeholder="Ask me anything about Appwrite...",
            label_visibility="collapsed"
        )

    with col2:
        submitted = st.form_submit_button(
            "Ask",
            disabled=st.session_state.is_processing
        )

st.markdown('</div>', unsafe_allow_html=True)

# Process user input
if submitted and user_input and not st.session_state.is_processing:
    st.session_state.chat_history.append(("You", user_input))
    st.session_state.is_processing = True
    st.rerun()

if st.session_state.is_processing and st.session_state.chat_history:
    last_message = st.session_state.chat_history[-1]
    if last_message[0] == "You":
        user_query = last_message[1]

        state = {
            "query": user_query,
            "chat_history": st.session_state.chat_history[:-1],
            "question": user_query,
            "docs": [],
            "answer": ""
        }

        try:
            with st.spinner("🧠 Analyzing Appwrite docs..."):
                result = app.invoke(state)

            st.session_state.chat_history = result["chat_history"]
            st.session_state.message_count += 1

        except Exception as e:
            error_message = f"Oops! WriteWise encountered an error: {str(e)}. Let's try that again!"
            st.session_state.chat_history.append(("WriteWise", error_message))

        finally:
            st.session_state.is_processing = False
            st.rerun()

# Floating clear chat button
if st.session_state.chat_history:
    if st.button("🗑️", key="clear_chat", help="Clear conversation", type="secondary"):
        st.session_state.chat_history = []
        st.session_state.message_count = 0
        st.rerun()

st.markdown('</div>', unsafe_allow_html=True)

# Enhanced JavaScript for better UX
st.markdown("""
<script>
// Smooth auto-scroll
function smoothScrollToBottom() {
    const chatContainer = document.querySelector('.chat-container');
    if (chatContainer) {
        chatContainer.scrollTo({
            top: chatContainer.scrollHeight,
            behavior: 'smooth'
        });
    }
}

// Enhanced input focus
function enhanceInput() {
    const input = document.querySelector('input[type="text"]');
    if (input) {
        input.focus();

        // Add enter key support
        input.addEventListener('keydown', function(e) {
            if (e.key === 'Enter' && !e.shiftKey) {
                e.preventDefault();
                const submitBtn = document.querySelector('button[kind="formSubmit"]');
                if (submitBtn && !submitBtn.disabled) {
                    submitBtn.click();
                }
            }
        });
    }
}

// Suggestion card interactions
function setupSuggestions() {
    document.querySelectorAll('.suggestion-card').forEach(card => {
        card.addEventListener('click', function() {
            const title = this.querySelector('h4').textContent;
            const input = document.querySelector('input[type="text"]');
            if (input) {
                let suggestion = '';
                switch(title) {
                    case '🗄️ Database Queries':
                        suggestion = 'How do I create and query a collection in Appwrite?';
                        break;
                    case '🔐 Authentication':
                        suggestion = 'How does user authentication work in Appwrite?';
                        break;
                    case '📁 Storage & Files':
                        suggestion = 'How do I upload and manage files in Appwrite storage?';
                        break;
                    case '⚡ Cloud Functions':
                        suggestion = 'How do I create and deploy cloud functions in Appwrite?';
                        break;
                }
                input.value = suggestion;
                input.focus();
            }
        });
    });
}

// Initialize on load
document.addEventListener('DOMContentLoaded', function() {
    smoothScrollToBottom();
    enhanceInput();
    setupSuggestions();
});

// Observe changes and maintain scroll
const observer = new MutationObserver(function(mutations) {
    mutations.forEach(function(mutation) {
        if (mutation.type === 'childList') {
            setTimeout(smoothScrollToBottom, 100);
        }
    });
});

const chatContainer = document.querySelector('.chat-container');
if (chatContainer) {
    observer.observe(chatContainer, { childList: true, subtree: true });
}
</script>
""", unsafe_allow_html=True)