import streamlit as st
from lida import Manager, TextGenerationConfig, llm
from lida.datamodel import Goal
import os
import pandas as pd

st.set_page_config(
    page_title="Stile Demo",
    page_icon="📊",
)

from dotenv import load_dotenv

load_dotenv(override=True)

# Step 1 - Get OpenAI API key
openai_key = os.getenv("OPENAI_API_KEY")

message = st.chat_message("assistant")
message.write("Hello, how may I help you today?")


selected_method = {"label": "llm",
         "description":
         "Uses the LLM to generate annotate the default summary, adding details such as semantic types for columns and dataset description"}

lida = Manager(text_gen=llm("openai", api_key=openai_key))

textgen_config = TextGenerationConfig(
        n=1,
        temperature=0,
        model="gpt-3.5-turbo",
        use_cache=True)

summary = lida.summarize(
        "compiled.csv",
        summary_method=selected_method,
        textgen_config=textgen_config)

def response_handler(prompt):
    new_goal = Goal(question=prompt, visualization=prompt, rationale="")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# React to user input
if prompt := st.chat_input("What is up?"):
    # Display user message in chat message container
    st.chat_message("user").markdown(prompt)
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})



    response = response_handler(prompt)
    # Display assistant response in chat message container
    with st.chat_message("assistant"):
        st.markdown(response)
    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": response})

