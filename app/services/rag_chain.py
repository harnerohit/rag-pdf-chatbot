import time
from functools import lru_cache

from langchain_groq import ChatGroq
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate

from app.core.config import settings
from app.core.logger import get_logger
from app.models.response import SourceChunk
from app.services.vectorstore import query_documents

logger = get_logger(__name__)

PROMPT = ChatPromptTemplate.from_template(
    """You are a document Q&A assistant.

Answer strictly using the provided context.

Rules:
- Do NOT use outside knowledge.
- Do NOT guess or make assumptions.
- If the answer is not present in the context, reply exactly:
  "I couldn't find that in the document."

Context:
{context}

Question:
{question}

Answer:
"""
)


@lru_cache
def get_llm():
    return ChatGroq(
        model=settings.llm_model,
        api_key=settings.groq_api_key,
        temperature=settings.temperature,
        max_tokens=settings.max_tokens,
    )


def format_docs(docs_with_scores):
    return "\n\n".join(
        doc.page_content for doc, _ in docs_with_scores
    )


def get_answer(doc_id: str, question: str):
    # Retrieve relevant chunks
    retrieval_start = time.time()

    results = query_documents(
        doc_id=doc_id,
        question=question,
        k=settings.retriever_top_k,
    )

    if not results:
        raise FileNotFoundError(
            f"No indexed content found for doc_id={doc_id}"
        )

    logger.info(
        f"Retrieval completed in "
        f"{time.time() - retrieval_start:.2f}s "
        f"({len(results)} chunks)"
    )

    # Generate answer
    generation_start = time.time()

    chain = PROMPT | get_llm() | StrOutputParser()

    answer = chain.invoke(
        {
            "context": format_docs(results),
            "question": question,
        }
    )

    logger.info(
        f"LLM generation completed in "
        f"{time.time() - generation_start:.2f}s"
    )

    # Build structured source response
    sources = [
        SourceChunk(
            doc_id=doc_id,
            filename=doc.metadata.get("filename", "Unknown"),
            page=doc.metadata.get("page"),
            chunk_index=doc.metadata.get("chunk_index", index),
            snippet=doc.page_content[:150] + "...",
            score=float(score),
        )
        for index, (doc, score) in enumerate(results)
    ]

    return answer, sources