"use client";

import { useState } from "react";
import { Download, MoreVertical, Share2 } from "lucide-react";
import { AssistantMessage } from "@/components/chat/AssistantMessage";
import { ChatComposer } from "@/components/chat/ChatComposer";
import { TypingIndicator } from "@/components/chat/TypingIndicator";
import { UserMessage } from "@/components/chat/UserMessage";
import { UnavailableTooltip } from "@/components/ui/UnavailableTooltip";
import type { AskResponse } from "@/services/api";

export type ChatMessage = Pick<AskResponse, "answer" | "sources" | "retrieved_chunks"> & {
  question: string;
};

type ChatWindowProps = {
  error: string | null;
  isThinking: boolean;
  messages: ChatMessage[];
  onAsk: (question: string) => void;
};

export function ChatWindow({ error, isThinking, messages, onAsk }: ChatWindowProps) {
  const [question, setQuestion] = useState("");

  function submitQuestion() {
    onAsk(question);
    if (question.trim()) setQuestion("");
  }

  return (
    <main aria-busy={isThinking} className="relative flex min-w-0 flex-1 flex-col bg-surface motion-safe:animate-[fade-in_300ms_ease-out]">
      <header className="hidden h-16 items-center justify-between border-b bg-surface/80 px-16 backdrop-blur-md md:flex">
        <div className="flex items-center gap-4 text-[13px] leading-[1.4] text-on-surface-variant">
          <span>
            Project: <strong className="font-semibold text-on-surface">Neural Architecture</strong>
          </span>
          <span className="size-1 rounded-full bg-outline-variant" />
          <span>Last analyzed 2 mins ago</span>
        </div>
        <div className="flex items-center gap-1">
          <HeaderAction label="Share"><Share2 /></HeaderAction>
          <HeaderAction label="Download"><Download /></HeaderAction>
          <HeaderAction label="More options"><MoreVertical /></HeaderAction>
        </div>
      </header>

      <div className="min-h-0 flex-1 overflow-y-auto px-6 py-12 pb-44 md:px-16">
        <div aria-live="polite" className="mx-auto flex w-full max-w-3xl flex-col gap-12">
          {messages.length === 0 ? (
            <div className="pt-24 text-center text-lg leading-[1.7] text-on-surface-variant">
              Ask a question to begin exploring this document.
            </div>
          ) : null}

          {messages.map((message, index) => (
            <div className="flex flex-col gap-12 motion-safe:animate-[fade-in_250ms_ease-out]" key={`${message.question}-${index}`}>
              <UserMessage>{message.question}</UserMessage>
              <AssistantMessage answer={message.answer} />
            </div>
          ))}

          {isThinking ? <TypingIndicator /> : null}
        </div>
      </div>

      <ChatComposer error={error} isThinking={isThinking} onQuestionChange={setQuestion} onSubmit={submitQuestion} question={question} />
    </main>
  );
}

function HeaderAction({ children, label }: { children: React.ReactNode; label: string }) {
  return (
    <UnavailableTooltip message="Available in a future update">
      <button aria-disabled="true" aria-label={`${label}. Available in a future update`} className="cursor-not-allowed rounded-lg p-2 text-on-surface-variant opacity-55" disabled tabIndex={-1} type="button">
        {children}
      </button>
    </UnavailableTooltip>
  );
}
