import streamlit as st
import requests

st.set_page_config(page_title="Newsletter Platform", layout="centered")

st.title("📰 Custom Newsletter Platform")

BASE_URL = "http://localhost:5000"

# -------------------------
# DEFAULT SESSION VALUES
# -------------------------
if "language" not in st.session_state:
    st.session_state["language"] = "Sanskrit"

# -------------------------
# USER REGISTRATION FORM
# -------------------------
st.header("👤 User Registration")

with st.form("user_form"):
    first_name = st.text_input("First Name")
    last_name = st.text_input("Last Name")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")

    category = st.selectbox(
        "Select Category",
        ["Tech News", "Sports News", "Business News", "Education News",
         "Health News", "Bollywood News", "Financial Market News"]
    )

    interests = st.text_input("Interests (AI, Health, Agriculture)")
    frequency = st.selectbox("Newsletter Frequency", ["Daily", "Weekly"])

    # ✅ Language Selection
    language = st.selectbox(
        "Preferred Language",
        ["Sanskrit", "English", "Hindi", "Marathi"]
    )

    submitted = st.form_submit_button("Register User")

if submitted:
    if email and first_name and last_name:
        try:
            res = requests.post(f"{BASE_URL}/register", json={
                "first_name": first_name,
                "last_name": last_name,
                "email": email,
                "password": password,
                "category": category,
                "interests": interests,
                "frequency": frequency,
                "language": language
            })

            st.success(res.json().get("message", "User Registered Successfully"))

            # ✅ Store in session
            st.session_state["email"] = email
            st.session_state["language"] = language

        except:
            st.error("❌ Backend not running or error occurred")
    else:
        st.warning("⚠️ Please fill required fields")

# -------------------------
# SCRAPE ARTICLE
# -------------------------
st.header("🔍 Scrape Article")

url = st.text_input("Enter Article URL")

if st.button("Scrape Content"):
    if url:
        try:
            res = requests.post(f"{BASE_URL}/scrape", json={"url": url})
            content = res.json().get("content", "")

            st.text_area("Extracted Content", content, height=200)

            st.session_state["content"] = content

        except:
            st.error("❌ Error scraping article")
    else:
        st.warning("⚠️ Please enter a URL")

# -------------------------
# SUMMARIZE CONTENT
# -------------------------
st.header("🤖 Summarize Content")

if st.button("Generate Summary"):
    content = st.session_state.get("content", "")

    if content:
        try:
            res = requests.post(f"{BASE_URL}/summarize", json={
                "content": content,
                "language": st.session_state.get("language", "Sanskrit")
            })

            summary = res.json().get("summary", "")

            st.success("✅ Summary Generated")
            st.write(summary)

            st.session_state["summary"] = summary

        except:
            st.error("❌ Error generating summary")
    else:
        st.warning("⚠️ No content available. Scrape first!")

# -------------------------
# SEND EMAIL
# -------------------------
st.header("📧 Send Newsletter")

if st.button("Send Email"):
    email = st.session_state.get("email", "")
    summary = st.session_state.get("summary", "")

    if email and summary:
        try:
            res = requests.post(f"{BASE_URL}/send-email", json={
                "email": email,
                "content": summary,
                "language": st.session_state.get("language", "Sanskrit")
            })

            st.success(res.json().get("message", "Email sent successfully"))

        except:
            st.error("❌ Error sending email")
    else:
        st.warning("⚠️ Email or summary missing. Complete previous steps first.")