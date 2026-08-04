import requests
import streamlit as st

API_URL = "http://127.0.0.1:8000"

st.set_page_config(
    page_title="RAG PDF Q&A Bot",
    page_icon="📄",
    layout="wide",
)

# ---------------------- Custom CSS ----------------------
st.markdown(
    """
<style>
.main {
    padding-top: 1rem;
}

.block-container {
    padding-top: 2rem;
}

.upload-box {
    padding:20px;
    border-radius:12px;
    background:#1e1e1e;
    border:1px solid #333;
}

.answer-box{
    padding:18px;
    border-radius:10px;
    background:#0f172a;
    border-left:5px solid #4CAF50;
}

.source-box{
    padding:12px;
    border-radius:10px;
    background:#202020;
}

.metric-card{
    padding:10px;
    border-radius:10px;
    background:#202020;
}
</style>
""",
    unsafe_allow_html=True,
)

# ---------------------- Sidebar ----------------------

with st.sidebar:
    st.title("📄 RAG PDF Bot")
    st.markdown("---")

    st.markdown(
        """
### Tech Stack

- FastAPI
- LangChain
- ChromaDB
- HuggingFace Embeddings
- Groq LLM
- Streamlit
"""
    )

    st.markdown("---")

    if "doc_id" in st.session_state:
        st.success("Document Indexed")
        st.code(st.session_state["doc_id"])

# ---------------------- Header ----------------------

st.title("📄 RAG PDF Q&A Bot")

st.caption(
    "Upload a PDF, ask questions, and receive grounded answers with source attribution."
)

st.markdown("---")

# ---------------------- Upload ----------------------

uploaded_file = st.file_uploader(
    "Upload PDF",
    type=["pdf"],
)

if uploaded_file:

    files = {
        "file": (
            uploaded_file.name,
            uploaded_file,
            "application/pdf",
        )
    }

    with st.spinner("Indexing PDF..."):

        response = requests.post(
            f"{API_URL}/upload",
            files=files,
        )

    if response.ok:

        data = response.json()

        st.session_state["doc_id"] = data["doc_id"]

        st.success("✅ PDF uploaded and indexed successfully!")

        c1, c2, c3 = st.columns(3)

        c1.metric("Pages", data["pages"])
        c2.metric("Chunks", data["chunks_indexed"])
        c3.metric("Status", "Indexed")

        with st.expander("📄 Document Information", expanded=True):

            st.write(f"**Filename:** {data['filename']}")
            st.write(f"**Document ID:** `{data['doc_id']}`")

    else:
        st.error("Failed to upload PDF.")

st.markdown("---")

# ---------------------- Question ----------------------

question = st.text_input(
    "Ask a question",
    placeholder="Example: What is Retrieval-Augmented Generation?",
)

if st.button("🚀 Ask", use_container_width=True):

    if "doc_id" not in st.session_state:
        st.error("Please upload a PDF first.")

    elif question.strip() == "":
        st.warning("Please enter a question.")

    else:

        with st.spinner("Thinking..."):

            response = requests.post(
                f"{API_URL}/ask",
                json={
                    "doc_id": st.session_state["doc_id"],
                    "question": question,
                },
            )

        if response.ok:

            result = response.json()

            st.markdown("## 🤖 Answer")

            st.markdown(
                f"""
<div class="answer-box">

{result["answer"]}

</div>
""",
                unsafe_allow_html=True,
            )

            st.markdown("")

            st.info(
                f"Retrieved **{result['retrieved_chunks']}** relevant chunks."
            )

            st.markdown("## 📚 Sources")

            for i, source in enumerate(result["sources"], start=1):

                with st.expander(
                    f"Source {i} | Page {source['page']}"
                ):

                    st.write(
                        f"**Filename:** {source['filename']}"
                    )

                    st.write(
                        f"**Chunk Index:** {source['chunk_index']}"
                    )

                    st.write(
                        f"**Similarity Score:** `{source['score']:.4f}`"
                    )

                    st.write("**Snippet:**")

                    st.code(source["snippet"])

        else:
            st.error("Failed to generate answer.")