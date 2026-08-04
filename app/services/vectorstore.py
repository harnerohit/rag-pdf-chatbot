from langchain_chroma import Chroma

from app.core.config import settings
from app.services.embedding import get_embedding_function

_vectordb = None


def get_vectorstore():
    global _vectordb

    if _vectordb is None:
        _vectordb = Chroma(
            collection_name="pdf_documents",
            embedding_function=get_embedding_function(),
            persist_directory=settings.chroma_persist_directory,
        )

    return _vectordb


def add_documents(doc_id: str, filename: str, chunks) -> int:
    for i, chunk in enumerate(chunks):
        chunk.metadata["doc_id"] = doc_id
        chunk.metadata["filename"] = filename
        chunk.metadata["page"] = chunk.metadata.get("page")
        chunk.metadata["chunk_index"] = i

    get_vectorstore().add_documents(chunks)

    return len(chunks)


def query_documents(doc_id: str, question: str, k: int):
    return get_vectorstore().similarity_search_with_score(
        question,
        k=k,
        filter={"doc_id": doc_id},
    )


def delete_document(doc_id: str) -> bool:
    vectordb = get_vectorstore()

    existing = vectordb.get(where={"doc_id": doc_id})

    if not existing or not existing.get("ids"):
        return False

    vectordb.delete(where={"doc_id": doc_id})

    return True