
# Task: Add RAGAS Evaluation to `rag-pdf-chatbot`

## Context (read this first, don't ask me to re-explain)

This is an existing, working RAG project called `rag-pdf-chatbot`. Stack:
- Backend: FastAPI, LangChain, ChromaDB (vector store), Groq (LLM inference), fastembed (embeddings)
- Frontend: React (the `streamlit_app.py` at repo root is dead code — ignore it, don't touch it unless asked)
- Package management: `uv` (has `pyproject.toml` + `uv.lock`), also has a `requirements.txt`

Current folder structure:
```
rag-pdf-chatbot/
├── app/
│   ├── api/
│   ├── core/
│   ├── models/
│   ├── services/      ← the retriever + RAG chain live somewhere in here
│   └── utils/
├── frontend/
│   └── ...
├── .env.example
├── .gitignore
├── .python-version
├── README.md
├── pyproject.toml
├── requirements.txt
├── streamlit_app.py    ← dead code, React is the real frontend
└── uv.lock
```

**Goal:** add a RAGAS evaluation setup that measures `faithfulness` and `answer_relevancy`
of the RAG pipeline's answers, without restructuring or touching any existing app code.
This should be a self-contained addition.

## Confirmed facts (from a prior read-only investigation — do not re-derive these)

- **Entry point:** `app/services/rag_chain.py::get_answer(doc_id: str, question: str)`
  → returns `tuple[str, list[SourceChunk]]` (answer string, source chunks). It internally
  calls `app/services/vectorstore.py::query_documents(doc_id, question, k)` for retrieval,
  then `prompt | llm | StrOutputParser()`. Not fused — but you don't need to call
  `query_documents` separately; `get_answer`'s returned `SourceChunk` list already gives you
  the retrieved context for that same call.
- **`SourceChunk` field name is NOT yet confirmed.** Open its definition (likely in
  `app/models/`) and check the actual attribute that holds the chunk text (candidates:
  `.content`, `.text`, `.chunk_text`) before writing `contexts = [c.<field> for c in chunks]`.
  Do not guess — read the model.
- **`get_answer` requires a `doc_id`.** This app is per-document — a PDF must already be
  ingested into Chroma with a known `doc_id` before you can call `get_answer` against it.
  Find an existing ingested `doc_id` (check the ingestion endpoint/test fixtures/Chroma data)
  or ingest a fixed test PDF first. `eval_questions.json` must carry a `doc_id` per question,
  not just a bare question string (see Step 3, updated below).
- **LLM:** `langchain_groq.ChatGroq`, model `openai/gpt-oss-120b` (configurable via
  `LLM_MODEL` in `app/core/config.py`) — use this exact model for the RAGAS judge LLM too,
  not `llama-3.3-70b-versatile`.
- **Embeddings:** `langchain_community.embeddings.fastembed.FastEmbedEmbeddings`,
  model `BAAI/bge-small-en-v1.5`. Reuse this directly for `answer_relevancy`'s embeddings
  requirement — do not add HuggingFace/sentence-transformers/torch.
- **Dependencies are already installed.** `ragas` (0.4.3) and `datasets` (5.0.1) are already
  declared and locked in `pyproject.toml`/`uv.lock`. **Skip Step 2 below entirely.**
- **`requirements.txt` is stale and unsafe to install from** — it still lists
  `langchain-huggingface`, `sentence-transformers`, and `torch==2.13.0` (pre-dates the
  FastEmbed migration) and is missing `fastembed`. Do not run
  `pip install -r requirements.txt`. Use `uv sync` / `uv run` instead. Flag the stale file
  as a cleanup item but do not fix it unless asked — out of scope for this task.
- **`SourceChunk` text field is `snippet: str` (in `app/models/response.py`) — and it's
  TRUNCATED to ~150 characters.** Do not use it for RAGAS `contexts`. A truncated context
  will produce unreliable `faithfulness` scores since the judge can't verify claims the
  snippet cut off. Instead, call `query_documents(doc_id, question, k)` directly for eval
  purposes and use `doc.page_content` (the full text) from each `(Document, score)` tuple
  it returns. This means retrieval runs twice per question (once inside `get_answer`, once
  standalone for full contexts) — acceptable for an offline eval script, not something to
  "optimize away" by reusing `get_answer`'s truncated snippets.
- **Match the real `k`.** Before writing `ragas_eval.py`, grep `app/services/rag_chain.py`
  for the `k` value it passes to `query_documents` internally, and use that exact same value
  in the standalone `query_documents` call below — otherwise the eval measures a different
  retrieval depth than production actually uses.
- **Real ingested `doc_id` for eval:** `a86ab0b9-1203-47db-8aae-69d3f957a2de`
  (`Sample_RAG_Document.pdf`, 4 indexed chunks, Chroma collection `pdf_documents`). Use this
  in `eval_questions.json`. Note there are only 4 chunks total — don't write questions that
  assume content beyond what's actually in that PDF. New docs can be ingested via
  `POST /upload`, which returns a fresh `doc_id` (generated via `uuid.uuid4()`).

## Target folder structure after this change

```
rag-pdf-chatbot/
├── app/
│   └── ... (unchanged)
├── evals/                          ← NEW
│   ├── ragas_eval.py                ← NEW: runs the evaluation
│   ├── eval_questions.json          ← NEW: 15-20 test questions
│   └── results/                     ← NEW: gitignored, stores run output
│       └── .gitkeep
├── frontend/
│   └── ... (unchanged)
├── .env.example                    ← unchanged (no new secrets needed; reuses existing Groq key)
├── .gitignore                      ← EDIT: add "evals/results/*" (keep .gitkeep)
├── README.md                       ← EDIT: add short "## Evaluation" section
├── pyproject.toml                  ← unchanged (ragas + datasets already present)
├── requirements.txt                ← unchanged (do not install from this file — it's stale)
└── ... (rest unchanged)
```

## Step-by-step instructions

### Step 1 — Confirm the one remaining unknown
Grep `app/services/rag_chain.py` for the `k` value passed to `query_documents` internally,
and use that exact value in Step 4's standalone `query_documents` call. Everything else
about the entry points, schema, and doc_id is already confirmed above.

### Step 2 — Skip
Dependencies already exist (see confirmed facts above). Just run `uv sync` if the venv
isn't already up to date. Do not touch `requirements.txt`.

### Step 3 — Create `evals/eval_questions.json`
Since `get_answer` is per-document, use the real ingested doc confirmed above:
`doc_id = "a86ab0b9-1203-47db-8aae-69d3f957a2de"` (`Sample_RAG_Document.pdf`, only 4 chunks
— keep questions scoped to what's actually in that PDF, don't invent content it doesn't
have). Format:
```json
[
  {"doc_id": "a86ab0b9-1203-47db-8aae-69d3f957a2de", "question": "..."},
  {"doc_id": "a86ab0b9-1203-47db-8aae-69d3f957a2de", "question": "..."}
]
```
With only 4 chunks, 8-12 varied questions is more realistic than 15-20 — beyond that you're
mostly re-testing the same chunks. If broader coverage matters later, ingest a second PDF
via `POST /upload` and mix in its `doc_id` too.

### Step 4 — Create `evals/ragas_eval.py`
```python
import json
from pathlib import Path

from app.services.rag_chain import get_answer
from app.services.vectorstore import query_documents

from ragas import evaluate
from ragas.metrics import faithfulness, answer_relevancy
from ragas.llms import LangchainLLMWrapper
from ragas.embeddings import LangchainEmbeddingsWrapper
from langchain_groq import ChatGroq
from langchain_community.embeddings.fastembed import FastEmbedEmbeddings
from datasets import Dataset

QUESTIONS_PATH = Path(__file__).parent / "eval_questions.json"
RESULTS_DIR = Path(__file__).parent / "results"
RESULTS_DIR.mkdir(exist_ok=True)

# Match whatever k value rag_chain.py actually uses internally (confirmed in Step 1) —
# do not leave this at a guessed default.
K = None  # <- set this from the grep in Step 1

def build_dataset():
    items = json.loads(QUESTIONS_PATH.read_text())
    rows = []
    for item in items:
        doc_id, question = item["doc_id"], item["question"]

        # Full-text contexts, NOT get_answer's truncated SourceChunk.snippet:
        results = query_documents(doc_id, question, K)
        contexts = [doc.page_content for doc, _score in results]

        answer, _source_chunks = get_answer(doc_id, question)  # snippets discarded, unused
        rows.append({"question": question, "contexts": contexts, "answer": answer})
    return Dataset.from_list(rows)

def main():
    judge_llm = LangchainLLMWrapper(ChatGroq(model="openai/gpt-oss-120b"))
    judge_embeddings = LangchainEmbeddingsWrapper(
        FastEmbedEmbeddings(model_name="BAAI/bge-small-en-v1.5")
    )

    dataset = build_dataset()
    result = evaluate(
        dataset,
        metrics=[faithfulness, answer_relevancy],
        llm=judge_llm,
        embeddings=judge_embeddings,
    )

    print(result)
    (RESULTS_DIR / "latest.json").write_text(json.dumps(result.to_pandas().to_dict(), indent=2))

if __name__ == "__main__":
    main()
```

Set `K` from Step 1's grep result before running — do not leave it as `None`. Nothing else
in this file should need guessing; every value came from the investigation, not a placeholder.

### Step 5 — `.gitignore`
Add:
```
evals/results/*
!evals/results/.gitkeep
```

### Step 6 — README
Add a short section:
```markdown
## Evaluation
RAG answer quality is measured with [RAGAS](https://github.com/explodinggym/ragas)
(`faithfulness`, `answer_relevancy`). Run:
    python evals/ragas_eval.py
Results are written to `evals/results/latest.json`.
```

### Step 7 — Run it
```
python evals/ragas_eval.py
```
Report back the faithfulness and answer_relevancy scores.

## Constraints
- Do not modify anything inside `app/` or `frontend/` unless strictly necessary to expose
  the retriever/answer functions (e.g. adding a public wrapper function is fine; changing
  chain logic is not).
- Do not touch `streamlit_app.py` — it's known dead code, out of scope for this task.
- Keep the evaluation fully separate from the shipped application code.
