import streamlit as st
import pandas as pd
import gspread
from gspread_auth import GSpreadAuth
import hashlib
from datetime import datetime

SHEET_ID = "1ktpsVs_4qYWRXnnPMIQTQxLG2LC5Pp9rdDYFLcbkXOY"  # 🔁 Replace with your actual sheet ID
SHEET_NAME = "Users"

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def get_sheet():
    gc = GSpreadAuth().authorize()
    sh = gc.open_by_key(SHEET_ID)
    worksheet = sh.worksheet(SHEET_NAME)
    return worksheet

def get_users_df():
    sheet = get_sheet()
    data = sheet.get_all_records()
    return pd.DataFrame(data)

def register_user(email, password):
    df = get_users_df()
    if email in df["email"].values:
        return False, "User already exists"
    sheet = get_sheet()
    hashed_pw = hash_password(password)
    sheet.append_row([email, hashed_pw])
    return True, "Registration successful"

def login_user(email, password):
    df = get_users_df()
    hashed = hash_password(password)
    user_row = df[(df["email"] == email) & (df["password"] == hashed)]
    return (not user_row.empty), "Login successful" if not user_row.empty else "Invalid credentials"

# --- Session ---
if "user" not in st.session_state:
    st.session_state.user = None
if "posts" not in st.session_state:
    st.session_state.posts = []

st.set_page_config(page_title="MySocialApp", layout="centered")
st.title("📱 MySocialApp")

# --- Auth UI ---
if not st.session_state.user:
    st.header("🔐 Login / Register")
    auth_choice = st.radio("Choose option:", ["Login", "Register"])
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")

    if auth_choice == "Register":
        if st.button("Register"):
            success, msg = register_user(email, password)
            st.success(msg) if success else st.error(msg)
    else:
        if st.button("Login"):
            success, msg = login_user(email, password)
            if success:
                st.session_state.user = email
                st.success(f"Welcome, {email}!")
            else:
                st.error(msg)
    st.stop()

# --- Logged In ---
st.sidebar.success(f"Logged in as: {st.session_state.user}")
if st.sidebar.button("Logout"):
    st.session_state.user = None
    st.experimental_rerun()

# --- Post Form ---
with st.form("new_post"):
    st.subheader("Create a Post")
    content = st.text_area("What's on your mind?", height=100, placeholder="Write something...")
    post_btn = st.form_submit_button("Post")

    if post_btn:
        if content:
            post = {
                "username": st.session_state.user,
                "content": content,
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "likes": 0
            }
            st.session_state.posts.insert(0, post)
            st.success("✅ Post published!")
        else:
            st.error("Post content cannot be empty.")

st.markdown("---")
st.subheader("📰 Recent Posts")

if st.session_state.posts:
    for i, post in enumerate(st.session_state.posts):
        with st.container():
            st.markdown(f"**@{post['username']}** · _{post['timestamp']}_")
            st.write(post['content'])

            # Like button
            like_btn = st.button(f"❤️ {post['likes']} Like(s)", key=f"like_{i}")
            if like_btn:
                st.session_state.posts[i]['likes'] += 1
                st.experimental_rerun()

            st.markdown("---")
else:
    st.info("No posts yet. Be the first to post something!")
