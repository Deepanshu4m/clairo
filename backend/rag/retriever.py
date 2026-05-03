import chromadb
from pathlib import Path

CHROMA_PATH = Path(__file__).resolve().parent / "chroma_store"

def get_career_context(query: str, n_results: int = 3) -> str:
    client = chromadb.PersistentClient(path=str(CHROMA_PATH))
    collection = client.get_or_create_collection(name="career_knowledge")

    results = collection.query(
        query_texts=[query],
        n_results=n_results,
    )

    docs = results["documents"][0] if results["documents"] else []
    return "\n\n".join(docs)