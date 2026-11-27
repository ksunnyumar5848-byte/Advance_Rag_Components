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
        if document.metadata.get("file_name")==source_name

    ]

    if not selected:
        FileNotFoundError(f"file name : {source_name} are the not loaded ")
    spliter=RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP,
        separators=["\n\n", "\n", ". ", " ", ""]
        
    )

    chunks=spliter.split_documents(selected)

    print("information the document ")
    print(f"chunk size : {CHUNK_SIZE}")
    print(f"chunk overlap : {CHUNK_OVERLAP}")
    print(f"source name it file name  : {source_name}")
    print(f"chunk charcater it means sentance in the doucument {selected[0].page_content} ")
    print(f"this is actul chunk : {len(chunks)}")

    for index , chunk in enumerate(chunks):
        text=chunk.page_content.strip()

        print(f"chunk : {index } characters {len(text)}  {count_token(text)} <- this text into token")

    print_banner("where neabring chunk overlap ")
    print(
            f"The overlap setting is {CHUNK_OVERLAP} characters. LangChain copies a "
            "previous piece into the next chunk only when that piece is no longer "
            "than the overlap. A whole paragraph longer than the overlap is not copied, "
            "so some boundaries share no text."
        )

    for index in range(len(chunks) -1):
        current=chunks[index].page_content.strip()
        following=chunks[index+1].page_content.strip()

        shared=0
        for size in range(1,min(len(current),len(following))+1):
            if current[-size:] == following[:size]:
                shared = size
                print(f"\nChunk {index} -> chunk {index + 1} | shared characters: {shared}")
                print(f"End of chunk {index}:   {current[-90:]}")
                print(f"Start of chunk {index + 1}: {following[:90]}")
    print(
            "\nNotice that a heading can land in one chunk while its first rule "
            "lands in the next. Structure-aware chunking is the lesson that repairs that."
        )


if __name__ == "__main__":
    main()

