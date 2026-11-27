import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))


from langchain_text_splitters import RecursiveCharacterTextSplitter
from rag_utils import count_token,Load_Documnet ,print_banner
from config import CHUNK_OVERLAP, CHUNK_SIZE

def main():
    print("recursive character printing ")
    print("this script are not call the gemini api ")

    print(f" chunk size of the sentance : {CHUNK_SIZE} \n")

    print(f"chunk overlap of the sentance : {CHUNK_OVERLAP}")

    source_name="hr_leave_policy.txt"

    selected=[
        document 
        for document in Load_Documnet()
        if document.metedata.get("file_name")==source_name

    ]

    if not selected:
        FileNotFoundError(f"file name : {source_name} are the not loaded ")

