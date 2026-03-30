import sys 
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import streamlit as st
from auth import login, create_user
from chat import handle_chat
from services.memory import get_history
from utils.helpers import load_pdf
from core.vector_store import create_vector_store

st.set_page_config(page_title="Smart AI Assistant", layout="wide")


if "user" not in st.session_state:
    st.session_state.user = None

if "chat_selected" not in st.session_state:
    st.session_state.chat_selected = None

if "query_input" not in st.session_state:
    st.session_state.query_input = ""

if "clear_input_flag" not in st.session_state:
    st.session_state.clear_input_flag = False


if "last_q" not in st.session_state:
    st.session_state.last_q = None

if "last_r" not in st.session_state:
    st.session_state.last_r = None


if not st.session_state.user:

    st.title("🔐 Smart AI Assistant")

    tab1, tab2 = st.tabs(["Login", "Register"])

    with tab1:
        st.subheader("Login")

        username = st.text_input("Username", key="login_user")
        password = st.text_input("Password", type="password", key="login_pass")

        if st.button("Login"):
            if login(username, password):
                st.session_state.user = username
                st.success("✅ Login successful!")
                st.rerun()
            else:
                st.error("❌ Invalid credentials")

    with tab2:
        st.subheader("Create Account")

        username = st.text_input("Username", key="reg_user")
        password = st.text_input("Password", type="password", key="reg_pass")

        if st.button("Register"):
            if username and password:
                success = create_user(username, password)

                if success:
                    st.success("✅ Account created! Please login.")
                else:
                    st.error("❌ Username already exists")
            else:
                st.warning("⚠️ Enter all fields")


else:

    st.sidebar.title(f"👋 {st.session_state.user}")

    if st.sidebar.button("➕ New Chat"):
        st.session_state.chat_selected = None
        st.session_state.query_input = ""
        st.session_state.last_q = None
        st.session_state.last_r = None
        st.rerun()

    if st.sidebar.button("🚪 Logout"):
        st.session_state.clear()
        st.rerun()

    st.sidebar.divider()


    history = get_history(st.session_state.user)

    st.sidebar.subheader("📜 History")

    for chat_id, q, r in history:
        if st.sidebar.button(q[:30], key=f"chat_{chat_id}"):
            st.session_state.chat_selected = (q, r)
            st.session_state.last_q = None
            st.session_state.last_r = None
            st.session_state.query_input = q
            st.rerun()


    st.title("💬 Chat Assistant")


    if st.session_state.chat_selected:
        q, r = st.session_state.chat_selected

        st.markdown("### 🧑 You")
        st.write(q)

        st.markdown("### 🤖 AI")
        st.markdown(r)

        st.divider()


    if st.session_state.last_q and st.session_state.last_r:
        st.markdown("### 🧑 You")
        st.write(st.session_state.last_q)

        st.markdown("### 🤖 AI")
        st.markdown(st.session_state.last_r)

        st.divider()


    uploaded_file = st.file_uploader("📄 Upload PDF (Optional)", type="pdf")

    if uploaded_file:
        with st.spinner("Processing PDF..."):
            text = load_pdf(uploaded_file)
            st.session_state.vector_store = create_vector_store(text)
            st.success("✅ PDF ready!")


    if st.session_state.clear_input_flag:
        st.session_state.query_input = ""
        st.session_state.clear_input_flag = False


    query = st.text_input("Ask something...", key="query_input")


    if st.button("Ask"):
        if query:
            with st.spinner("Thinking..."):
                response = handle_chat(
                    st.session_state.user,
                    query,
                    st.session_state.get("vector_store")
                )

                # ✅ STORE RESPONSE (KEY FIX)
                st.session_state.last_q = query
                st.session_state.last_r = response

                st.session_state.clear_input_flag = True

             


    st.markdown(
        "<script>window.scrollTo(0, document.body.scrollHeight);</script>",
        unsafe_allow_html=True
    )