import streamlit as st
import os
import requests

CHATBOT_URL = os.getenv("CHATBOT_URL", "http://localhost:8000/gif-search")


def card(urls):
    figures = [f"""
        <figure style="margin-top: 5px; margin-bottom: 5px; !important;">
            <img src="{url}" style="width: 130px; height: 100px; padding-left: 5px; padding-right: 5px" >
        </figure>
    """ for url in urls]
    return st.markdown(f"""
        <div style="display: flex; flex-flow: row wrap; text-align: center; justify-content: center;">
        {''.join(figures)}
        </div>
    """, unsafe_allow_html=True)


st.write("""
## ⚡️ AI-Powered GIF Search ⚡️
""")

query = st.text_input("What are you looking for?", "")

if query != "":
    with st.spinner(text="Similarity Searching..."):
        data = {"text": query}
        response = requests.post(CHATBOT_URL, json=data)
        urls = []
        if response.status_code == 200:
            urls = response.json()["output"]

        else:
            output_text = """An error occurred while processing your message.
                    Please try again or rephrase your message."""
    with st.spinner(text="Fetching GIFs 🚀🚀🚀"):
        card(urls)
