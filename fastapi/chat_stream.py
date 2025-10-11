from groq import Groq
from dotenv import load_dotenv
import os
import json
from fastapi import FastAPI
from pydantic import BaseModel, Field
from fastapi.responses import StreamingResponse

load_dotenv()

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


def groq_response_stream():
    full_response = ""
    completions = client.chat.completions.create(
        model="openai/gpt-oss-20b",
        messages=conversations,
        temperature=0,
        stream=True
    )

    for chunk in completions:
        if chunk.choices[0].delta.content:
            text_chunk = chunk.choices[0].delta.content
            full_response += text_chunk
            yield text_chunk
    
    completions.append({"role" : "assistant", "content" : full_response})

class Query(BaseModel):
    query: str = Field(..., min_length=2)


@app.get("/health")
def home():
    return {"message": "Application is live"}


@app.post("/chat") 
def ask_question(chat: Query):
    conversations.append({"role": "user", "content": chat.query})
    response = groq_response()
    conversations.append({"role" : "assistant", "content": response})
    return {"answer": response}

@app.post('/chat-stream')
def ask_question_stream(chat: Query):
    conversations.append({"role": "user", "content": chat.query})
    return StreamingResponse(
        groq_response_stream(),
        media_type="text/plain"
    )
