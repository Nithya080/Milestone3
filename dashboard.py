import streamlit as st
from scanner import scan_url, calculate_risk
from email_alert import send_email

st.set_page_config(page_title="Vulnerability Scanner", layout="centered")

st.title("🔍 Vulnerability Scanner")

url = st.text_input("Enter URL")

if st.button("Scan"):
    if not url:
        st.warning("Please enter a URL")
    else:
        results = scan_url(url)
        score = calculate_risk(results)

        st.subheader("Results")
        st.write(results)

        st.subheader("Risk Score")
        st.metric("Score", score)

        # Severity count
        severity_count = {}
        for r in results:
            severity_count[r["severity"]] = severity_count.get(r["severity"], 0) + 1

        st.subheader("Severity Distribution")
        st.bar_chart(severity_count)

        # 🔥 AUTO EMAIL TRIGGER
        send_email(results, url, score)