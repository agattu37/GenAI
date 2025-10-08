import streamlit as st
from groq import Groq
from dotenv import load_dotenv
import os
import json

load_dotenv()

# A simple chatbot assistant based of Groq LLM models
client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)

def groq_response():
    completions = client.chat.completions.create(
        model="openai/gpt-oss-20b",
        messages=st.session_state.messages,
        temperature=0
    )

    return completions.choices[0].message.content

def main():
    st.title("Simple Chatbot Assistant")
    st.subheader("A simple chatbot as Assistant for all your queries")
    st.divider()

    if "messages" not in st.session_state:
        prompt = "Act as helpful assistant"
        st.session_state.messages = [{"role" : "system", "content" : prompt}]

    for message in st.session_state.messages:
        if message["role"] != "system":
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

    query = st.chat_input("Ask your query here ... ?")

    if query:
        with st.chat_message("user"):
            st.markdown(query)

        st.session_state.messages.append({"role" : "user", "content" : query})

        response = groq_response()

        with st.chat_message("assistant"):
            st.markdown(response)

        st.session_state.messages.append({"role" : "assistant", "content" : response})

        with open("conversation.json", "w") as file:
            file.write(json.dumps(st.session_state.messages, indent=4))

main()
