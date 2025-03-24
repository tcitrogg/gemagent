import streamlit as st
import getpass
import os
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate

st.set_page_config(page_title="Gemagen", page_icon="👾")

if "GEMINI_API_KEY" not in os.environ:
    os.environ["GEMINI_API_KEY"] = getpass.getpass("Enter your Google AI API key: ")

GEMINI_API_KEY = os.environ["GEMINI_API_KEY"]


# Instantiation
LLM = ChatGoogleGenerativeAI(
    model="gemini-1.5-pro",
    temperature=0,
    max_tokens=None,
    timeout=None,
    max_retries=2,
    google_api_key=GEMINI_API_KEY
    # other params...
)


# prompting

prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You are a helpful assistant that instructs and plan out learning schedule for learn the Rust programming language",
        ),
        ("human", "{input}"),
    ]
)

chain = prompt | LLM

DEFAULT_PROMPT = "You are a helpful assistant that instructs and plan out learning schedule for learn the Rust programming language"


# using the langchain to handle responses
def handle_response(userinput: str, USER_PROMPT=""):
    # ai_msg = chain.invoke(
    #     {
    #         "input_language": "English",
    #         "output_language": "Japanese",
    #         "input": userinput,
    #     }
    # )
    if (bool(USER_PROMPT) is False):
        system_prompt = DEFAULT_PROMPT
    else:
        system_prompt = USER_PROMPT
    messages = [
        (
            "system",
            system_prompt,
        ),
        ("human", "{input}"),
    ]
    ai_msg = LLM.invoke(messages)
    return ai_msg

# ~ GUI
sidebar = st.sidebar
sidebar.header("Gemagen")
sidebar.chat_message(f"Gemagen", avatar="👾").markdown(f"DEFAULT PROMPT = `{DEFAULT_PROMPT}`")
sidebar.chat_input("Write a prompt for Gemagen")
sidebar.chat_message("arkitect", avatar="🫀").markdown("[yours Tcitrogg](https://bnierimi.vercel.app)")

with st.container():
    # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []
        
        
    # Display chat messages from history on app rerun
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

if userinput := st.chat_input("Say something"):
    
    # Display user message in chat message container
    st.chat_message("user").markdown(userinput)
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": userinput})
    
    response = handle_response(userinput).content
    # Display assistant response in chat message container
    gemagen_ass = st.chat_message("assistant", avatar="👾")
    with gemagen_ass:
        st.markdown(response)
    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": response})