import streamlit as st
import requests

st.set_page_config(page_title="Free Public AI Chatbot", page_icon="💬")
st.title("🤖 My Custom Free ChatGPT")
st.caption("Running 100% free open-source AI")

if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Hello! Ask me anything. I am completely free to use!"}
    ]

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

if user_query := st.chat_input("Type your message here..."):
    st.session_state.messages.append({"role": "user", "content": user_query})
    st.chat_message("user").write(user_query)

    with st.chat_message("assistant"):
        response_placeholder = st.empty()
        
        # Using a fast, free conversational AI model from Meta
        API_URL = "https://huggingface.co"
        payload = {"inputs": {"text": user_query}}
        
        try:
            response = requests.post(API_URL, json=payload)
            res_data = response.json()
            
            # Extract the text answer smoothly from the free API return format
            if isinstance(res_data, list) and len(res_data) > 0 and "generated_text" in res_data[0]:
                ai_response = res_data[0]["generated_text"]
            elif "generated_text" in res_data:
                ai_response = res_data["generated_text"]
            else:
                ai_response = "I am processing. Please say that one more time!"
                
            response_placeholder.write(ai_response)
            st.session_state.messages.append({"role": "assistant", "content": ai_response})
        except Exception as e:
            response_placeholder.write("Warming up my free brain servers... please try sending your message again!")
