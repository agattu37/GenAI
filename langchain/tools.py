from langchain.chat_models import init_chat_model
import os
from dotenv import load_dotenv
from pydantic import BaseModel, Field

load_dotenv()

model = init_chat_model("gemini-2.5-flash", model_provider="google_genai")

class GetWeather(BaseModel):
    """Get the current weather in a given location"""

    location: str = Field(..., description="The city and state, e.g. San Francisco, CA")

model_with_tools = model.bind_tools([GetWeather])

res = model_with_tools.invoke("what's the weather in Tacoma")

print(res)
