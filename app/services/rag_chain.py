import re
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


import re


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