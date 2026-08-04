export type UploadedDocument = {
  doc_id: string;
  filename: string;
  pages: number;
  chunks_indexed: number;
};

export type SourceChunk = {
  doc_id: string;
  filename: string;
  page: number | null;
  chunk_index: number;
  snippet: string;
  score: number | null;
};

export type AskResponse = {
  answer: string;
  sources: SourceChunk[];
  retrieved_chunks: number;
};

const API_URL = process.env.NEXT_PUBLIC_API_URL ?? "http://127.0.0.1:8000";

export async function uploadPDF(file: File): Promise<UploadedDocument> {
  const formData = new FormData();
  formData.append("file", file);

  let response: Response;
  try {
    response = await fetch(`${API_URL}/upload`, {
      method: "POST",
      body: formData,
    });
  } catch {
    throw new Error("Unable to reach the server. Check that the API is running.");
  }

  if (!response.ok) {
    const payload = await response.json().catch(() => null);
    throw new Error(typeof payload?.detail === "string" ? payload.detail : "Unable to upload the PDF.");
  }

  return response.json();
}

export async function askQuestion(docId: string, question: string): Promise<AskResponse> {
  let response: Response;
  try {
    response = await fetch(`${API_URL}/ask`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ doc_id: docId, question }),
    });
  } catch {
    throw new Error("Unable to reach the server. Check that the API is running.");
  }

  if (!response.ok) {
    const payload = await response.json().catch(() => null);
    throw new Error(typeof payload?.detail === "string" ? payload.detail : "Unable to answer that question.");
  }

  return response.json();
}

export async function deleteDocument(docId: string): Promise<void> {
  let response: Response;
  try {
    response = await fetch(`${API_URL}/delete/${encodeURIComponent(docId)}`, {
      method: "DELETE",
    });
  } catch {
    throw new Error("Unable to reach the server. Check that the API is running.");
  }

  if (!response.ok) {
    const payload = await response.json().catch(() => null);
    throw new Error(typeof payload?.detail === "string" ? payload.detail : "Unable to delete the document.");
  }
}
