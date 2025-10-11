from my_movprod_controller import get_movies_by_filter
from groq import Groq
from dotenv import load_dotenv
import os
import json

load_dotenv()

client = Groq(
    api_key = os.getenv("GROQ_API_KEY")
)


tools = [
    {
        "type" : "function",
        "function" : {
            "name" : "get_movies_by_titles",
            "description" : "Queries the from database for movie titles. Useful for answering questions about movie titles, year, genre. The query is case-insensitive search on the title name.",
            "parameters" : {
                "type" : "object",
                "properties" : {
                    "title" : {
                        "type" : "string",
                        "description" : "The search term for the movie name"
                    },
                    "plot" : {
                        "type" : "string",
                        "description" : "The movie plot filter. Like 'A young man, unaccustomed to children, must accompany a young girl.'"
                    },
                    "year" : {
                        "type" : "object",
                        "properties" : {
                            "$gte" : {
                                "type" : "number",
                                "description" : "Movie release date greater than equal to. Should always be greater than or equal to 1900. "
                            },
                            "$lte" : {
                                "type" : "number",
                                "description" : "Movie release date less than equal to. Should never be less than 2025. "
                            }
                        }
                    }
                },
                "required" : []
            },
        }
    }
]

# {
#     "query" : "",
#     "category" : "",
#     "price" : {
#         "$gte" : "",
#         "$lte" : ""
#     }
# }


def get_available_functions(function_name):
    available_functions = {
        "get_movies_by_titles" : get_movies_by_filter 
    }

    return available_functions[function_name]

def get_movgroq_response(query):

    response = client.chat.completions.create(
        model="openai/gpt-oss-20b",
        messages=[
            {"role" : "system", "content" : "Act as a product recommendation engine"},
            {"role" : "user", "content" : query}    
        ],
        tools=tools
    )

    tool_calls = response.choices[0].message.tool_calls

    print(tool_calls)

    if tool_calls:

        for tool_call in tool_calls:

            function_name = tool_call.function.name
            function_to_call = get_available_functions(function_name)
            function_args = json.loads(tool_call.function.arguments)

            function_response = function_to_call(**function_args)

            return function_response
        
    else:
        return response.choices[0].message.content
