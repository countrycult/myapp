# -*- coding: utf-8 -*-
"""app.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1EEudf2i-75hSLcUyNMj3sjWFddfk1rai
"""

import streamlit as st
from datetime import datetime

# App config
st.set_page_config(page_title="MySocialApp", layout="centered")
st.title("📱 MySocialApp")

# Initialize session state
if "posts" not in st.session_state:
    st.session_state.posts = []

# --- Post Form ---
with st.form("new_post"):
    st.subheader("Create a Post")
    username = st.text_input("Username", placeholder="Enter your name")
    content = st.text_area("What's on your mind?", height=100, placeholder="Write something...")
    post_btn = st.form_submit_button("Post")

    if post_btn:
        if username and content:
            post = {
                "username": username,
                "content": content,
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "likes": 0
            }
            st.session_state.posts.insert(0, post)
            st.success("✅ Post published!")
        else:
            st.error("Username and content cannot be empty.")

st.markdown("---")

# --- Feed ---
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