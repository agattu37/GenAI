from groq import Groq
from dotenv import load_dotenv
import os
import json
from fastapi import FastAPI
from pydantic import BaseModel, Field

load_dotenv()

# Get the GROQ_API_KEY
client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)

app = FastAPI()

conversations = []

def groq_response():
    completions = client.chat.completions.create(
        model="openai/gpt-oss-20b",
        messages=conversations,
        temperature=0,
    )

    return completions.choices[0].message.content

class Query(BaseModel):
    query: str = Field(..., min_length=2)

# the health route
@app.get("/health")
def home():
    return {"message": "Application is live"}

# the chat function route
@app.post("/chat") 
def ask_question(chat: Query):
    conversations.append({"role": "user", "content": chat.query})
    response = groq_response()
    conversations.append({"role" : "assistant", "content": response})
    return {"answer": response}
