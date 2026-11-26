import sys
import os
import json
import warnings
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
warnings.filterwarnings(
    "ignore",
    category=DeprecationWarning
)

# this module dwonload the document 

from langchain_community.document_loaders import (
    Docx2txtLoader,
    PyPDFLoader,
    TextLoader,
    CSVLoader
)

def print_banner(title:str):
    """
    this print visible Heading 
    """
    line="="*72
    print(f"\n {line} \n {title} \n {line} \n")


print_banner("GEN AI Enggineer")


def Document_label(document:Document) ->str:
    file_name=document.metadata.get("file_name","document")
    chunk_index=document.metadata.get("chunk")

    if not chunk_index:
        return file_name
    return f"file name is : {file_name}  chunk_index : {chunk_index}"

def count_token(text:str)->int:
    """
      your text convet into number and return token number 
    """
    import tiktoken
    encoder=tiktoken.get_encoding("cl100k_base")
    return len(encoder.encode(text)
)


