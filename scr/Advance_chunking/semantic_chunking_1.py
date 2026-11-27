import sys
from pathlib import Path

import numpy as np
from langchain_text_splitters import RecursiveCharacterTextSplitter

PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))


from config import CHUNK_SIZE, CHUNK_OVERLAP,SIMILARITY_BREAKPOINT_PERCENTILE
from rag_utils import count_token, Load_Documnet, print_banner
from llm_client import get_embedding_model


def splict_sentance(text:str):
    import re

    normalized=text.replace("\n"," ")
    pieces = re.split(r"(?<=[.!?])\s+", normalized)

    return [piece.strip() for piece in pieces if len(piece.strip()) > 40]


def cosieon_simalarity(left,right):
    """
        Calculate how similar two vectors are based on the angle between them.
    
        Returns:
            1.0  -> Vectors point in exactly the same direction.
            0.0  -> Vectors are perpendicular or one of them is empty.
           -1.0  -> Vectors point in exactly opposite directions.
    
        Example:
            left  = [1, 0] & right = [1, 0]
            Output = 1.0
    
            left  = [1, 0] & right = [0, 1]
            Output = 0.0
    """

    left_vector=np.asarray(left,dtype=float)
    right_vector=np.asarray(right,dtype=float)

    denominator = float(np.linalg.norm(left_vector) * np.linalg.norm(right_vector))
    if denominator == 0:
            return 0.0
    return float(np.dot(left_vector, right_vector) / denominator) 

