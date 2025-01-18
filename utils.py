import streamlit as st

def write_message(role, content, save = True):
    """
    This is a helper function that saves a message to the
     session state and then writes a message to the UI
    """
    # Append to session state
    if save:
        st.session_state.messages.append({"role": role, "content": content})

    # Write to UI
    with st.chat_message(role):
        st.markdown(content)

def generate_response(user_input, bot):
    """
    This is a helper function that invokes the .respond
    method of the agent to get the response
    """
    return bot.respond(user_input)