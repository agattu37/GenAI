import streamlit as st
from openai import OpenAI
from dotenv import load_dotenv
import os

# A module which allows to choose a model from the given set of models
# Allows you to select an Action, to have a simple conversation or with a context
# For context based conversation choose the radio button 'instructions' and
# provide the context in the field Instructions.
# Though this modules allows to select a LLM model, but mostly it works with 
# gpt-4.1-nano, for others it will rate limit.

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

openai_client = OpenAI(
    api_key=OPENAI_API_KEY
)

openai_model = "gpt-4.1-nano"

class OpenAIChat:

    def generate_simple_answer(self, query, model):
        response = openai_client.responses.create(
            model=model,
            input=query,
            temperature=1 
        )
        return response.output_text
    
    # Get a list of models
    def get_models_list(self):
        models = openai_client.models.list()
        model_list = [model.id for model in models.data]
        return model_list
    
    # Generte a response
    def generate_answer_with_instructions(self, instructions, query, model):
        response = openai_client.responses.create(
            model=model,
            input=query,
            instructions=instructions 
        )
        return response.output_text

    

def main():
    openai_chat = OpenAIChat()
    st.title("Welcome to simple conversations")
    selected_page = ""

    # Create a sidebar with 2 sets of choices: 
    # Simple Conversation or with Instructions
    with st.sidebar:
        st.title("Choose your action")
        selected_page = st.radio("Choose your action", ["Simple Conversation", "Instructions"])

    # Select a model, give a query, and get a response
    if selected_page == "Simple Conversation":
        models = openai_chat.get_models_list()
        query = st.text_input("Enter your query")
        select_model = st.selectbox("Select your model", tuple(models))
        if query and select_model:
            answer = openai_chat.generate_simple_answer(query, select_model)
            st.write(answer)

    # Can provide a context to the query
    if selected_page == "Instructions":
        instruction = st.text_area("Enter your instruction")
        models = openai_chat.get_models_list()
        query = st.text_input("Enter your query")
        select_model = st.selectbox("Select your model", tuple(models))

        # Create an answer button
        button = st.button("Answer")
        if query and select_model and instruction and button:

            # Add a spinner
            with st.spinner("Generating..."):
                answer = openai_chat.generate_answer_with_instructions(instruction, query, select_model)
                st.write(answer)



main()
