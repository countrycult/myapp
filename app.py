import streamlit as st
import pandas as pd
import gspread
from gspread_auth import GSpreadAuth
import hashlib

SHEET_ID = "1AbCDefGHijkLmNoPQRstuVWXYZ1234567890"  # Replace with yours
SHEET_NAME = "Users"

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def get_sheet():
    gc = GSpreadAuth().authorize()  # Will prompt once to authenticate via browser
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

# Session state
if "user" not in st.session_state:
    st.session_state.user = None

# UI
st.title("🔐 Login/Register with Google Sheets")

if not st.session_state.user:
    option = st.radio("Choose:", ["Login", "Register"])
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")

    if option == "Register":
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
else:
    st.sidebar.success(f"Logged in as {st.session_state.user}")
    if st.sidebar.button("Logout"):
        st.session_state.user = None
        st.experimental_rerun()
