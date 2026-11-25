import os
import sys
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings
from config import CHAT_MODEL ,CHAT_REASONING_EFFORT,EMBEDDING_MODEL


def require_gemini_api_key():
    api_key=os.getenv("GEMINI_API_KEY")

    if not api_key:
        raise RuntimeError(
            "you have not the api in the .env file ",
            "api key are not found "
            )
    return api_key


def get_chat_model() -> ChatGoogleGenerativeAI:
    """
      this methods are the nothin simple create the modal for gemini modal jaise variable name modal 
      hamlog karte tia 
    """

    return ChatGoogleGenerativeAI(
        model=CHAT_MODEL,
        api_keey=require_gemini_api_key(),
        temperature=0,
        maxtoken=1000,
        reasoning_effort=CHAT_REASONING_EFFORT
    )

    





