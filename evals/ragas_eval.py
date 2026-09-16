import json
import sys
import time
from types import ModuleType
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from datasets import Dataset
from langchain_community.embeddings.fastembed import FastEmbedEmbeddings
from langchain_groq import ChatGroq

# Ragas 0.4.3 imports this removed legacy class only for an isinstance check.
if "langchain_community.chat_models.vertexai" not in sys.modules:
    vertexai = ModuleType("langchain_community.chat_models.vertexai")
    vertexai.ChatVertexAI = type("ChatVertexAI", (), {})
    sys.modules[vertexai.__name__] = vertexai

from ragas import evaluate
from ragas.embeddings import LangchainEmbeddingsWrapper
from ragas.llms import LangchainLLMWrapper
from ragas.metrics import answer_relevancy, faithfulness
from ragas.run_config import RunConfig

import ragas.embeddings.base
class _DummyEvent:
    def __init__(self, *args, **kwargs): pass
ragas.embeddings.base.EmbeddingUsageEvent = _DummyEvent

from app.core.config import settings
from app.services.rag_chain import get_answer
from app.services.vectorstore import query_documents

QUESTIONS_PATH = Path(__file__).parent / "eval_questions.json"
RESULTS_DIR = Path(__file__).parent / "results"
RESULTS_DIR.mkdir(exist_ok=True)
K = 6


def build_dataset():
    items = json.loads(QUESTIONS_PATH.read_text())
    rows = []
    for item in items:
        doc_id, question = item["doc_id"], item["question"]
        results = query_documents(doc_id, question, K)
        contexts = [doc.page_content for doc, _score in results]
        answer, _source_chunks = get_answer(doc_id, question)
        rows.append({"question": question, "contexts": contexts, "answer": answer})
        # ponytail: fixed delay for Groq's 8k TPM limit; use provider-aware limiting if this grows.
        time.sleep(15)
    return Dataset.from_list(rows)


def main():
    judge_llm = LangchainLLMWrapper(
        ChatGroq(model="openai/gpt-oss-120b", api_key=settings.groq_api_key)
    )
    judge_embeddings = LangchainEmbeddingsWrapper(
        FastEmbedEmbeddings(model_name="BAAI/bge-small-en-v1.5")
    )
    answer_relevancy.strictness = 1

    result = evaluate(
        build_dataset(),
        metrics=[faithfulness, answer_relevancy],
        llm=judge_llm,
        embeddings=judge_embeddings,
        run_config=RunConfig(max_workers=1),
        raise_exceptions=True,
    )

    print(result)
    (RESULTS_DIR / "latest.json").write_text(
        json.dumps(result.to_pandas().to_dict(), indent=2)
    )


if __name__ == "__main__":
    main()
