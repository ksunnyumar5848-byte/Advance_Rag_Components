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
from config import(
    CHUNK_OVERLAP,
    CHUNK_SIZE,
    METADATA_FILE,
    EMBEDDING_MODEL,
    FAISS_INDEX_DIR,
    DOCUMENTS_DIR
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


def load_metedata_catalog():
    """
      this methods are load meta data form the matadata file  
    """
    if not METADATA_FILE.exists():
        raise FileNotFoundError(
            f"meta data are not found in your metadata file directory "
        )
    with METADATA_FILE.open(encoding="utf-8") as metadata_file:
        catalog=json.load(metadata_file)

    if not isinstance(catalog, dict):
            raise ValueError("documents.json must be an object keyed by file name.")
    
    return catalog


def Load_Documnet():
     
     """ this methods are simple load the document from the data folder 
        Load PDF, DOCX, TXT, and CSV files from data/documents
     """

     if not DOCUMENTS_DIR.exists():
          raise FileNotFoundError(
               f"you have not  documnet folder in the data folder "
          )
     catalog=load_metedata_catalog()

     documents=[]

     for path in sorted(DOCUMENTS_DIR.iterdir()):

        if not path.is_file() or path.name.startswith("."):
            continue
        suffix=path.suffix.lower()

        if suffix==".txt":
            loader=TextLoader(str(path), encoding="utf-8") 

        elif suffix==".pdf":
            loader=PyPDFLoader(str(path))

        elif suffix==".docx":
              loader=Docx2txtLoader(str(path))
        elif suffix==".csv":
              loader = CSVLoader(str(path), encoding="utf-8")

        else:
              print(f"unsupport file name please sikps bro  {path}")
              continue

          # this methods are find inside the meta data file name like pdf docx csv 
        file_metadata=catalog.get(path.name)

        if not file_metadata:
              raise KeyError(
                  f"your meta data folder inside no any documnet json "
              )
          
        for document in loader.load():
             # Catalog values win on shared keys such as "source", because the
             # loaders also use "source" for the file path.
            merged_metadata = dict(document.metadata)
            merged_metadata.update(file_metadata)
            merged_metadata["file_name"] = path.name
            merged_metadata["file_path"] = str(path)
            document.metadata = merged_metadata
            if document.page_content and document.page_content.strip():
                documents.append(document)
     if not documents:
            raise FileNotFoundError(f"No documents were loaded from {DOCUMENTS_DIR}")
    
     print(f"Loaded {len(documents)} document parts from {DOCUMENTS_DIR.name}/.")
     return documents






def split_documents(
          documents:list[Document],
          chunk_size:int=CHUNK_SIZE,
          chunk_overlap:int=CHUNK_OVERLAP
)->list[Document]:

     # you document are splict into sentance line of paragraph 

    spliter=RecursiveCharacterTextSplitter(
          chunk_siz=chunk_size,
          chunk_overlap=chunk_overlap,
          separators=["\n\n", "\n", ". ", " ", ""]
    )

    chunks=spliter.split_documents(documents)

    next_index: dict[str, int] = {}
    for chunk in chunks:
            chunk.metadata = dict(chunk.metadata)  # Create a copy of the metadata dictionary.
            file_name = chunk.metadata.get("file_name", "document")
            chunk.metadata["chunk_index"] = next_index.get(file_name, 0)  # Start at 0 for each file.
            next_index[file_name] = chunk.metadata["chunk_index"] + 1  # Increment the index for the next chunk.
    
        # Remove chunks that contain only whitespace or are empty.
    chunks = [chunk for chunk in chunks if chunk.page_content.strip()]
    print(
            f"Split those documents into {len(chunks)} chunks "
            f"({chunk_size} characters, {chunk_overlap} overlap)."
        )
    return chunks


def create_faisse_store(documents:list[Document]):
     from langchain_community.vectorstores import FAISS

     from llm_client import get_embedding_model

     if not documents:
        raise ValueError("Cannot build a FAISS index from an empty document list.")

     print(f"Embedding {len(documents)} passages with {EMBEDDING_MODEL}...")
     store = FAISS.from_documents(documents, get_embedding_model())
     print("In-memory FAISS index is ready.")
     return store

     



   
           
     

