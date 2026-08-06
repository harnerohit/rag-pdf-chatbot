# TEMP DEBUG - REMOVE AFTER RENDER INVESTIGATION
print("[startup] app.services.rag_chain: before re import", flush=True)
import re
print("[startup] app.services.rag_chain: after re import", flush=True)

print("[startup] app.services.rag_chain: before time import", flush=True)
import time
print("[startup] app.services.rag_chain: after time import", flush=True)

print("[startup] app.services.rag_chain: before lru_cache import", flush=True)
from functools import lru_cache
print("[startup] app.services.rag_chain: after lru_cache import", flush=True)

print("[startup] app.services.rag_chain: before ChatGroq import", flush=True)
from langchain_groq import ChatGroq
print("[startup] app.services.rag_chain: after ChatGroq import", flush=True)

print("[startup] app.services.rag_chain: before StrOutputParser import", flush=True)
from langchain_core.output_parsers import StrOutputParser
print("[startup] app.services.rag_chain: after StrOutputParser import", flush=True)

print("[startup] app.services.rag_chain: before ChatPromptTemplate import", flush=True)
from langchain_core.prompts import ChatPromptTemplate
print("[startup] app.services.rag_chain: after ChatPromptTemplate import", flush=True)

print("[startup] app.services.rag_chain: before settings import", flush=True)
from app.core.config import settings
print("[startup] app.services.rag_chain: after settings import", flush=True)

print("[startup] app.services.rag_chain: before logger import", flush=True)
from app.core.logger import get_logger
print("[startup] app.services.rag_chain: after logger import", flush=True)

print("[startup] app.services.rag_chain: before SourceChunk import", flush=True)
from app.models.response import SourceChunk
print("[startup] app.services.rag_chain: after SourceChunk import", flush=True)

print("[startup] app.services.rag_chain: before vectorstore import", flush=True)
from app.services.vectorstore import query_documents
print("[startup] app.services.rag_chain: after vectorstore import", flush=True)

print("[startup] app.services.rag_chain: before logger creation", flush=True)
logger = get_logger(__name__)
print("[startup] app.services.rag_chain: after logger creation", flush=True)

print("[startup] app.services.rag_chain: before prompt creation", flush=True)
PROMPT = ChatPromptTemplate.from_template(
    """
You are an intelligent document assistant.

Use ONLY the provided context.

Instructions:
- Never use outside knowledge.
- Never invent facts.
- When the user asks for:
  - a summary,
  - an overview,
  - what the document/PDF is about,
  - the main topic,
  summarize the retrieved context in your own words.
- You may combine information from multiple retrieved chunks.
- Only reply "I couldn't find that in the document." if the retrieved context contains no useful information related to the question.

Context:
{context}

Question:
{question}

Answer:
"""
)
print("[startup] app.services.rag_chain: after prompt creation", flush=True)


@lru_cache
def get_llm():
    return ChatGroq(
        model=settings.llm_model,
        api_key=settings.groq_api_key,
        temperature=settings.temperature,
        max_tokens=settings.max_tokens,
    )


def format_docs(docs_with_scores) -> str:
    """
    Format retrieved chunks into a structured context
    for the LLM.
    """

    formatted_chunks = []

    for index, (doc, _) in enumerate(docs_with_scores, start=1):
        formatted_chunks.append(
            f"Chunk {index}:\n{doc.page_content}"
        )

    return "\n\n".join(formatted_chunks)


print("[startup] app.services.rag_chain: before second re import", flush=True)
import re
print("[startup] app.services.rag_chain: after second re import", flush=True)


def rewrite_query(question: str) -> str:
    """
    Rewrite broad document-level questions into
    retrieval-friendly queries.
    """

    query = re.sub(
        r"[^\w\s]",
        "",
        question.lower().strip(),
    )

    summary_patterns = [
        ["what", "pdf", "about"],
        ["what", "document", "about"],
        ["tell", "document"],
        ["tell", "pdf"],
        ["overview"],
        ["summary"],
        ["summarize"],
        ["main", "topic"],
    ]

    for pattern in summary_patterns:
        if all(word in query for word in pattern):
            return "summarize the document"

    return question


def get_answer(doc_id: str, question: str):
    """
    Retrieve relevant context and generate an answer.
    """

    retrieval_question = rewrite_query(question)

    logger.info(f"Original Question : {question}")
    logger.info(f"Retrieval Query   : {retrieval_question}")

    retrieval_start = time.time()

    results = query_documents(
        doc_id=doc_id,
        question=retrieval_question,
        k=settings.retriever_top_k,
    )
    print("\n" + "=" * 80)
    print("RETRIEVED CHUNKS")
    print("=" * 80)
    
    for i, (doc, score) in enumerate(results, start=1):
        print(f"\nChunk {i} | Score: {score:.4f}")
        print("-" * 80)
        print(doc.page_content[:1000])
        print("-" * 80)

    if not results:
        raise FileNotFoundError(
            f"No indexed content found for doc_id={doc_id}"
        )

    logger.info(
        "Retrieval completed in %.2fs (%d chunks)",
        time.time() - retrieval_start,
        len(results),
    )

    generation_start = time.time()

    chain = PROMPT | get_llm() | StrOutputParser()

    answer = chain.invoke(
        {
            "context": format_docs(results),
            "question": question,
        }
    )

    logger.info(
        "LLM generation completed in %.2fs",
        time.time() - generation_start,
    )

    sources = []

    for index, (doc, score) in enumerate(results):

        snippet = (
            doc.page_content[:150] + "..."
            if len(doc.page_content) > 150
            else doc.page_content
        )

        sources.append(
            SourceChunk(
                doc_id=doc_id,
                filename=doc.metadata.get("filename", "Unknown"),
                page=doc.metadata.get("page"),
                chunk_index=doc.metadata.get(
                    "chunk_index",
                    index,
                ),
                snippet=snippet,
                score=float(score),
            )
        )

    return answer, sources
