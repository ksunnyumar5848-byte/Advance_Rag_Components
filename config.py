from pathlib import Path

PROJECT_ROOT=Path(__file__).resolve().parent

DATA_DIR = PROJECT_ROOT / "data"
DOCUMENTS_DIR = DATA_DIR / "documents"
METADATA_DIR = DATA_DIR / "metadata"
METADATA_FILE = METADATA_DIR / "documents.json"

# Optional folder used only if you call save_faiss_store / load_faiss_store.
FAISS_INDEX_DIR = PROJECT_ROOT / "faiss_index"

# OpenAI models. gpt-6-luna is a small, current chat model.
# reasoning_effort "none" lets us set temperature for repeatable classroom runs.
# text-embedding-3-small is the embedding model used for every vector index.
CHAT_MODEL = "gpt-6-luna"
CHAT_REASONING_EFFORT = "none"
EMBEDDING_MODEL = "text-embedding-3-small"

# Local cross-encoder used only by src/reranking/cross_encoder_reranking.py.
# The first run downloads this small model from Hugging Face.
CROSS_ENCODER_MODEL = "cross-encoder/ms-marco-MiniLM-L-6-v2"

# Recursive splitting is measured in characters, not tokens.
# Overlap keeps a few characters from the previous chunk so a sentence that
# crosses a boundary is still visible in both chunks.
CHUNK_SIZE = 800
CHUNK_OVERLAP = 120

# How many passages a normal search returns.
TOP_K = 4

# How many passages reranking and compression pull before they narrow the list.
CANDIDATE_K = 6

# Reciprocal Rank Fusion constant. Rank 1 contributes 1 / (RRF_K + 1).
RRF_K = 60

# Parent chunks are stored for the answer. Child chunks are what we search.
PARENT_CHUNK_SIZE = 1600
PARENT_CHUNK_OVERLAP = 150
CHILD_CHUNK_SIZE = 350
CHILD_CHUNK_OVERLAP = 40

# Sentence-window retrieval returns this many sentences on each side.
SENTENCE_WINDOW = 1

# Long-context scripts retrieve more passages, then stay inside a token budget.
LONG_CONTEXT_TOP_K = 8
TOKEN_BUDGET = 2200

# Semantic chunking starts a new chunk when neighboring sentences are less
# similar than this percentile of all neighboring pairs in the document.
SIMILARITY_BREAKPOINT_PERCENTILE = 30




