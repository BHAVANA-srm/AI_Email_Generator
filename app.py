import streamlit as st
import google.generativeai as genai
from dotenv import load_dotenv
import os
import datetime

# Load API Key
load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# Gemini Model
model = genai.GenerativeModel("gemini-2.5-flash")

# App Title
st.set_page_config(page_title="AI Email Assistant", page_icon="📧")
st.title("📧 AI Email Assistant")

# Tabs
tab1, tab2, tab3, tab4 = st.tabs([
    "Email Generator",
    "Grammar Checker",
    "Email Summarizer",
    "Reply Generator"
])

# -----------------------------
# EMAIL GENERATOR
# -----------------------------
with tab1:

    st.header("Generate Professional Emails")

    recipient = st.text_input("Recipient")

    purpose = st.text_area("Purpose of the Email")

    tone = st.selectbox(
        "Tone",
        ["Professional", "Friendly", "Formal", "Polite"]
    )

    language = st.selectbox(
        "Language",
        ["English", "Hindi", "Tamil", "French", "Spanish"]
    )

    if st.button("Generate Email"):

        prompt = f"""
        Write a complete email in {language}.

        Recipient: {recipient}
        Purpose: {purpose}
        Tone: {tone}

        Include:
        - Subject Line
        - Greeting
        - Email Body
        - Professional Closing
        """

        response = model.generate_content(prompt)

        st.subheader("Generated Email")
        st.markdown(response.text)

        with open("history.txt", "a", encoding="utf-8") as file:
            file.write(
                f"\n\n{'='*60}\n"
                f"TIME: {datetime.datetime.now()}\n\n"
                f"{response.text}\n"
            )

# -----------------------------
# GRAMMAR CHECKER
# -----------------------------
with tab2:

    st.header("Grammar Correction")

    grammar_text = st.text_area(
        "Enter text to correct"
    )

    if st.button("Correct Grammar"):

        prompt = f"""
        Correct grammar, spelling,
        punctuation, and sentence structure.

        Text:
        {grammar_text}
        """

        response = model.generate_content(prompt)

        st.subheader("Corrected Text")
        st.markdown(response.text)

# -----------------------------
# EMAIL SUMMARIZER
# -----------------------------
with tab3:

    st.header("Email Summarizer")

    email_text = st.text_area(
        "Paste email content"
    )

    if st.button("Summarize Email"):

        prompt = f"""
        Summarize the following email
        into concise bullet points.

        Email:
        {email_text}
        """

        response = model.generate_content(prompt)

        st.subheader("Summary")
        st.markdown(response.text)

# -----------------------------
# REPLY EMAIL GENERATOR
# -----------------------------
with tab4:

    st.header("Reply Email Generator")

    received_email = st.text_area(
        "Paste received email"
    )

    reply_tone = st.selectbox(
        "Reply Tone",
        ["Professional", "Friendly", "Formal", "Polite"]
    )

    if st.button("Generate Reply"):

        prompt = f"""
        Write a {reply_tone} reply
        to the following email.

        Email:
        {received_email}

        Include:
        - Subject
        - Greeting
        - Body
        - Closing
        """

        response = model.generate_content(prompt)

        st.subheader("Generated Reply")
        st.markdown(response.text)

# -----------------------------
# HISTORY VIEWER
# -----------------------------
st.divider()

st.subheader("📜 Email History")

if os.path.exists("history.txt"):
    with open("history.txt", "r", encoding="utf-8") as file:
        history = file.read()

    st.text_area(
        "Generated Emails",
        history,
        height=250
    )
else:
    st.info("No email history available yet.")