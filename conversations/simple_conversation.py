import streamlit as st
from openai import OpenAI
from dotenv import load_dotenv
import os

# A simple conversational module based on user input and response returned 
# by a LLM model. This can be run on local laptop.

load_dotenv()

# Read the open API key from the .env file
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

openai_client = OpenAI(
    api_key=OPENAI_API_KEY
)

# Use GPT 4.1 nano model
openai_model = "gpt-4.1-nano"

# Create an OpenAIChat class
class OpenAIChat:

# Create a function which itakes the user input query and genrates a response 
    def generate_simple_answer(self, query):
        response = openai_client.responses.create(
            model=openai_model,
            input=query,
            temperature=1 
        )
        return response.output_text
    
# Define main function
def main():
    openai_chat = OpenAIChat()

    # Create the tile for the UI page
    st.title("Welcome to simple conversations")

    query = st.text_input("Enter your query")

    if query:
        answer = openai_chat.generate_simple_answer(query)
        st.write(answer)

# Call the main function
main()
