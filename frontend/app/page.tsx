"use client";

import { useState } from "react";
import { AppShell } from "@/components/layout/AppShell";
import { ChatWindow } from "@/components/chat/ChatWindow";
import type { ChatMessage } from "@/components/chat/ChatWindow";
import { ContextPanel } from "@/components/layout/ContextPanel";
import { UploadEmptyState } from "@/components/upload/UploadEmptyState";
import { askQuestion, deleteDocument, uploadPDF } from "@/services/api";
import type { UploadedDocument } from "@/services/api";

export default function Home() {
  const [document, setDocument] = useState<UploadedDocument | null>(null);
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [error, setError] = useState<string | null>(null);
  const [isUploading, setIsUploading] = useState(false);
  const [isThinking, setIsThinking] = useState(false);
  const [isDeleting, setIsDeleting] = useState(false);

  async function handleUpload(file: File) {
    if (!file.name.toLowerCase().endsWith(".pdf")) {
      setError("Choose a PDF file to upload.");
      return;
    }

    setError(null);
    setIsUploading(true);

    try {
      setDocument(await uploadPDF(file));
      setMessages([]);
    } catch (uploadError) {
      setError(uploadError instanceof Error ? uploadError.message : "Unable to upload the PDF.");
    } finally {
      setIsUploading(false);
    }
  }

  async function handleAsk(question: string) {
    if (!question.trim()) {
      setError("Enter a question before sending it.");
      return;
    }

    if (!document) {
      setError("Upload a PDF before asking a question.");
      return;
    }

    setError(null);
    setIsThinking(true);

    try {
      const response = await askQuestion(document.doc_id, question.trim());
      setMessages((currentMessages) => [...currentMessages, { question: question.trim(), ...response }]);
    } catch (askError) {
      setError(askError instanceof Error ? askError.message : "Unable to answer that question.");
    } finally {
      setIsThinking(false);
    }
  }

  async function handleDelete() {
    if (!document) return;

    setError(null);
    setIsDeleting(true);

    try {
      await deleteDocument(document.doc_id);
      setDocument(null);
      setMessages([]);
    } catch (deleteError) {
      setError(deleteError instanceof Error ? deleteError.message : "Unable to delete the document.");
    } finally {
      setIsDeleting(false);
    }
  }

  const latestMessage = messages.at(-1);

  return (
    <AppShell
      contextPanel={
        document ? <ContextPanel document={document} isDeleting={isDeleting} onDelete={handleDelete} retrievedChunks={latestMessage?.retrieved_chunks ?? 0} sources={latestMessage?.sources ?? []} /> : null
      }
    >
      {document ? (
        <ChatWindow error={error} isThinking={isThinking} messages={messages} onAsk={handleAsk} />
      ) : (
        <UploadEmptyState error={error} isUploading={isUploading} onFileSelect={handleUpload} />
      )}
    </AppShell>
  );
}
