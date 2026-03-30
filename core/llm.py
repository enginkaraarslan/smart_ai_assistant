import os
import google.generativeai as genai
import streamlit as st

def get_api_key():
    try:
        return st.secrets["GEMINI_API_KEY"]  
    except:
        return os.getenv("GEMINI_API_KEY")  

genai.configure(api_key=get_api_key())


def get_llm():
    return genai.GenerativeModel("gemini-2.5-flash")