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

def get_embedding_model() -> GoogleGenerativeAIEmbeddings:
    """
    this methods are the create embedding because it 
    embedding are send into the vectore db 
    """
    return GoogleGenerativeAIEmbeddings(
        model=EMBEDDING_MODEL,
        api_key=require_gemini_api_key()
    )


def message_text(message):
    """
      here message text methods are a require the msg and 
      if msg inside the content and type a string 
    """

    content=getattr(message,"content",message)

    if isinstance(content,str):
        return content.strip() 

    pieces=[]


    if isinstance(content,str):

        for block in pieces:

            if isinstance(block,dict):
                """this are cheak content are dict then this text are content  
                   and access form the dic text or content and store the pieces list 
                """
                text=block.get("text") or block.get("content") or " "

                if text:
                    pieces.append(str(text))

            elif isinstance(block,str):
                pieces.append(block) # because this is all ready the string and store into the pieces list 

            else:
                text=getattr(block,"text"," ") # inside the content block and  text or empyth then push into the text 
                if text:
                    pieces.append(str(text))
        return "\n".join(pieces).strip()  # all the text are combine and new new line 



    





