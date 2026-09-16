# Archivalist
### AI-Powered PDF Research Assistant

> **Transform static documents into intelligent conversations.**

Archivalist is a modern Retrieval-Augmented Generation (RAG) application that enables users to upload PDF documents and interact with them through natural language. Instead of relying solely on an LLM's pre-trained knowledge, Archivalist grounds every response in the uploaded document, providing accurate, contextual, and source-backed answers.

---

## ✨ Overview

Large Language Models are powerful—but without context, they hallucinate.

Archivalist solves this by combining:

- 📄 Document Processing
- 🧠 Semantic Search
- 🗂️ Vector Database Retrieval
- 🤖 Large Language Models

The result is a research assistant that understands your documents instead of guessing.

---

# Demo

> *(Add screenshots or GIFs here after deployment)*

| Upload PDF | Ask Questions |
|------------|---------------|
| *(Screenshot)* | *(Screenshot)* |

| Source Citations | Document Intelligence |
|------------------|-----------------------|
| *(Screenshot)* | *(Screenshot)* |

---

# Features

### 📄 Intelligent PDF Processing

- Upload PDF documents
- Automatic text extraction
- Smart document chunking
- Metadata preservation

---

### 🧠 Semantic Retrieval

Instead of keyword search, Archivalist understands meaning using sentence embeddings.

Features include:

- Semantic similarity search
- Vector embeddings
- ChromaDB indexing
- Top-K context retrieval

---

### 🤖 AI-Powered Question Answering

Ask natural language questions like:

> What is this document about?

> Summarize this document.

> Explain RAG.

> What are the key concepts?

Every answer is generated using retrieved context from the uploaded document.

---

### 📚 Source-backed Responses

Every response includes:

- Source document
- Page number
- Retrieved chunk
- Context snippet

Helping users verify every generated answer.

---

### 🎨 Modern Research Workspace

Built with a premium editorial-inspired interface featuring:

- Responsive layout
- Minimal distraction design
- Document intelligence panel
- Elegant typography
- Accessibility improvements

---

# Architecture

```text
                PDF Upload
                     │
                     ▼
            PDF Loader (LangChain)
                     │
                     ▼
          Recursive Text Splitter
                     │
                     ▼
      HuggingFace Embeddings Model
                     │
                     ▼
               ChromaDB
                     │
          Semantic Retrieval
                     │
                     ▼
      Retrieved Context + Question
                     │
                     ▼
               Groq LLM
                     │
                     ▼
        Source-backed AI Response
```

---

# Tech Stack

## Frontend

- Next.js 16
- TypeScript
- Tailwind CSS
- shadcn/ui
- Lucide React

---

## Backend

- FastAPI
- LangChain
- ChromaDB
- HuggingFace Embeddings
- Groq API

---

## AI Stack

- Retrieval-Augmented Generation (RAG)
- Semantic Search
- Vector Embeddings
- Context Augmentation

---

# Project Structure

```text
RAG_PDF_Chatbot/

├── app/
│   ├── api/
│   ├── core/
│   ├── models/
│   ├── services/
│   └── utils/
│
├── frontend/
│   ├── app/
│   ├── components/
│   ├── services/
│   ├── styles/
│   └── public/
│
├── requirements.txt
├── pyproject.toml
├── uv.lock
└── README.md
```

---

# API Endpoints

## Upload Document

```http
POST /upload
```

Uploads a PDF and indexes it into the vector database.

---

## Ask Questions

```http
POST /ask
```

Returns:

- AI answer
- Source citations
- Retrieved chunks

---

## Delete Document

```http
DELETE /delete/{doc_id}
```

Removes an indexed document from the vector database.

---

# Local Setup

## Clone

```bash
git clone https://github.com/harnerohit/rag-pdf-chatbot.git

cd rag-pdf-chatbot
```

---

## Backend

```bash
uv sync

uv run uvicorn app.main:app --reload
```

---

## Frontend

```bash
cd frontend

npm install

npm run dev
```

---

## Environment Variables

Backend

```env
GROQ_API_KEY=your_groq_api_key
```

Frontend

```env
NEXT_PUBLIC_API_URL=http://127.0.0.1:8000
```

---

## Evaluation

RAG answer quality is measured with [RAGAS](https://github.com/explodinggym/ragas)
(`faithfulness`, `answer_relevancy`). Run:

    python evals/ragas_eval.py

Results are written to `evals/results/latest.json`.

# Why RAG?

Traditional LLMs rely only on pre-trained knowledge.

Archivalist retrieves relevant document context before generation, resulting in:

- Higher factual accuracy
- Lower hallucination
- Explainable responses
- Source-backed answers

---

# Future Improvements

- Multi-document conversations
- Chat history
- Authentication
- Streaming responses
- OCR support
- Hybrid search
- Drag-and-drop uploads
- Docker deployment
- Cloud vector database
- Multi-user workspaces

---

# Key Learnings

Building Archivalist involved practical experience with:

- FastAPI API development
- LangChain pipelines
- Embedding models
- Vector databases
- Semantic retrieval
- Prompt engineering
- Retrieval-Augmented Generation
- Modern React development
- Production UI architecture

---

# License

This project is licensed under the MIT License.

---

# Author

**Rohit Harne**

AI Engineer

GitHub: https://github.com/harnerohit

---

⭐ If you found this project interesting, consider giving it a star.
