import streamlit as st
from openai import OpenAI
import os

# Set up the webpage layout
st.set_page_config(page_title="Public AI Chatbot", page_icon="💬")
st.title("🤖 My Custom ChatGPT")
st.caption("A public chatbot built with Python and Streamlit")

# Securely fetch the API key from Streamlit's dashboard secrets
API_KEY = st.secrets.get("OPENAI_API_KEY")
client = OpenAI(api_key=API_KEY)

# Streamlit Session State keeps user chats separate from each other
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Hello! Ask me anything."}
    ]

# Display all previous messages in the chat UI
for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

# Handle new user input
if user_query := st.chat_input("Type your message here..."):
    st.session_state.messages.append({"role": "user", "content": user_query})
    st.chat_message("user").write(user_query)

    with st.chat_message("assistant"):
        response_placeholder = st.empty()
        
        # Call the OpenAI model
        completion = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a public chatbot assistant."}
            ] + st.session_state.messages
        )
        
        ai_response = completion.choices.message.content
        response_placeholder.write(ai_response)
        
    st.session_state.messages.append({"role": "assistant", "content": ai_response})
