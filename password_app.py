import streamlit as st
import re
import random
import string

# App config
st.set_page_config(page_title="🔐 Password Strength Meter", layout="centered")

# Session state for theme and password visibility
if "dark_mode" not in st.session_state:
    st.session_state.dark_mode = True

if "show_password" not in st.session_state:
    st.session_state.show_password = False

# Theme Toggle Button 🌗
theme_toggle = st.button("🌞 Switch to Light Mode" if st.session_state.dark_mode else "🌙 Switch to Dark Mode")
if theme_toggle:
    st.session_state.dark_mode = not st.session_state.dark_mode

# Background and text colors based on theme
if st.session_state.dark_mode:
    bg_color = "#0f0f0f"
    text_color = "#f0f0f0"
    title_glow = "#00f7ff"
else:
    bg_color = "#f5f5f5"
    text_color = "#0f0f0f"
    title_glow = "#0066ff"

# Custom CSS
st.markdown(f"""
<style>
    .stApp {{
        background-color: {bg_color};
        color: {text_color};
    }}
    .main-title {{
        font-size: 2.8em;
        text-align: center;
        color: {title_glow};
        text-shadow: 0 0 10px {title_glow}, 0 0 20px {title_glow};
        margin-bottom: 10px;
    }}
    .sub-text {{
        text-align: center;
        font-size: 1.1em;
        margin-bottom: 2rem;
        color: #888;
    }}
    .password-input input {{
        background-color: #202020;
        color: #00f7ff;
        border: 1px solid #00f7ff;
        border-radius: 8px;
        padding: 10px;
    }}
    .stButton > button {{
        background: linear-gradient(90deg, #00c2ff, #008cff);
        color: white;
        font-weight: bold;
        padding: 10px 20px;
        border-radius: 8px;
        border: none;
        transition: all 0.3s ease;
    }}
    .stButton > button:hover {{
        background: linear-gradient(90deg, #008cff, #00c2ff);
        box-shadow: 0 0 10px #00f7ff;
        transform: scale(1.05);
    }}
</style>
""", unsafe_allow_html=True)

# Title
st.markdown("<div class='main-title'>🔐 Password Strength Meter</div>", unsafe_allow_html=True)
st.markdown("<div class='sub-text'>Type a password to check its strength in real time! 🧠</div>", unsafe_allow_html=True)

# Password Input with Visibility Toggle 👁️
col1, col2 = st.columns([5, 1])
with col1:
    password = st.text_input("Enter your password:", type="default" if st.session_state.show_password else "password")
with col2:
    st.write("")  # spacing
    if st.button("👁️" if not st.session_state.show_password else "🙈", help="Toggle visibility"):
        st.session_state.show_password = not st.session_state.show_password

# Password Strength Checker
def check_password_strength(password):
    score = 0
    feedback = []

    blacklist = ["password123", "123456", "qwerty", "admin", "letmein"]
    if password.lower() in blacklist:
        return "❌ Blacklisted", 0, ["Avoid common passwords like 'password123'."]

    if len(password) >= 8:
        score += 1
    else:
        feedback.append("🔹 Use at least 8 characters.")

    if re.search(r"[A-Z]", password) and re.search(r"[a-z]", password):
        score += 1
    else:
        feedback.append("🔹 Include both uppercase & lowercase letters.")

    if re.search(r"\d", password):
        score += 1
    else:
        feedback.append("🔹 Add at least one number (0–9).")

    if re.search(r"[!@#$%^&*]", password):
        score += 1
    else:
        feedback.append("🔹 Use special characters like !@#$%^&*.")

    if not re.search(r"\s", password):
        score += 1
    else:
        feedback.append("🔹 Avoid spaces in passwords.")

    if score == 5:
        return "🔐 Strong", score, []
    elif score >= 3:
        return "⚠️ Moderate", score, feedback
    else:
        return "❌ Weak", score, feedback

# Password Generator
def generate_password(length=12):
    chars = string.ascii_letters + string.digits + "!@#$%^&*"
    return ''.join(random.choice(chars) for _ in range(length))

# Real-time Evaluation
if password:
    strength, score, feedback = check_password_strength(password)

    st.markdown(f"**📊 Strength:** `{strength}` | **💯 Score:** `{score}/5`")

    # Color Bar
    bar_color = "#ff4d4d"
    if score >= 5:
        bar_color = "#00cc66"
    elif score >= 3:
        bar_color = "#ffaa00"

    st.markdown(f"""
    <div style='margin-top:10px; height:25px; width:100%; background-color:#333; border-radius:10px;'>
        <div style='height:100%; width:{(score/5)*100}%; background-color:{bar_color}; border-radius:10px; transition:width 0.5s;'></div>
    </div>
    """, unsafe_allow_html=True)

    if feedback:
        st.warning("💡 Tips to improve your password:")
        for tip in feedback:
            st.markdown(f"- {tip}")
    else:
        st.success("✅ Your password is strong and secure!")

# Strong password button
st.markdown("---")
if st.button("✨ Generate Strong Password"):
    st.code(generate_password(), language="text")
