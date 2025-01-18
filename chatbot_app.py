import streamlit as st
from utils import write_message, generate_response
from main import bot

# Page Config
st.set_page_config("Chatbot", page_icon=":gear:")

# Set up Session State
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Hi, I'm  your  Chatbot!  How can I help you?"},
    ]

# Submit handler
def handle_submit(message):
    # Handle the response
    with st.spinner('Thinking...'):
        message = generate_response(message, bot)
        write_message('assistant', message)


# Display messages in Session State
for message in st.session_state.messages:
    write_message(message['role'], message['content'], save=False)

# Handle any user input
if question := st.chat_input("What is up?"):
    # Display user message in chat message container
    write_message('user', question)

    # Generate a response
    handle_submit(question)
