from pydantic import BaseModel, Field
from typing import Literal
from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate


class Intent(BaseModel):
    intent_type: Literal["Sales Inquiry", "Pricing Questions", "Support Request", "Spam", "Other"] = Field(
        description="The primary category of the email's intent"
    )
    is_sales_lead: bool = Field(
        description="A boolean flag indicating if this email presents a potential sales lead"
    )
    summary: str = Field(
        description="A bried, one-sentence summary of the email's intent"
    )

def classify_intent(email_content: str) -> Intent:
    """
    Used to clasify the intent of the email in a structured format
    """

    llm = ChatOllama(model="qwen2.5:latest")

    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", "You are an expert at classifying inbound business emails. Your goal is to determine the sender's intent and identify it is a sales lead. You must respond ONLY with the structured JSON object, no other text"),
            ("human", "Here is the email content to classify: ```{email_content}```")
        ]
    )

    structured_llm = llm.with_structured_output(Intent)

    chain = prompt | structured_llm

    response = chain.invoke({"email_content", email_content})

    return response


if __name__ == "__main__":
    print("--- Testing with a Sales Inquiry ---")
    sales_email = """
    Hi there,

    I saw your presentation on autonomous agents and was very impressed.
    We are a 50-person tech company and are looking for a solution to automate our lead follow-up.
    Could we schedule a 15-minute call next week to discuss our needs and see a demo?

    Best,
    Alex
    """
    sales_result = classify_intent(sales_email)
    print(sales_result)

    print("\n--- Testing with a Support Request ---")
    support_email = """
    Hello,

    I'm an existing customer and I can't seem to log into my account.
    I've tried resetting my password but I'm not receiving the reset email.
    Can you please help? My username is user@example.com.

    Thanks,
    Jane
    """
    support_result = classify_intent(support_email)
    print(support_result)

    print("\n--- Testing with Spam ---")
    spam_email = """
    CONGRATULATIONS!!! YOU HAVE WON A $1,000,000 LOTTERY. CLICK HERE TO CLAIM.
    """
    spam_result = classify_intent(spam_email)
    print(spam_result)
