import { ArrowUp, Paperclip } from "lucide-react";

type ChatComposerProps = {
  error: string | null;
  isThinking: boolean;
  onQuestionChange: (question: string) => void;
  onSubmit: () => void;
  question: string;
};

export function ChatComposer({ error, isThinking, onQuestionChange, onSubmit, question }: ChatComposerProps) {
  return (
    <div className="pointer-events-none absolute inset-x-0 bottom-0 bg-gradient-to-t from-surface via-surface to-transparent px-6 pb-6 pt-12 md:px-16">
      <div className="pointer-events-auto mx-auto max-w-3xl">
        <form
          aria-busy={isThinking}
          className="relative flex h-14 items-center rounded-full border bg-surface shadow-[0_8px_30px_rgb(0,0,0,0.06)] transition-all duration-300 focus-within:border-primary focus-within:shadow-[0_8px_30px_rgb(0,0,0,0.1)]"
          onSubmit={(event) => {
            event.preventDefault();
            onSubmit();
          }}
        >
          <button aria-label="Attach file" className="absolute left-2 flex size-10 items-center justify-center rounded-full text-on-surface-variant" disabled>
            <Paperclip className="size-5" strokeWidth={1.5} />
          </button>
          <input
            aria-describedby={error ? "chat-error" : undefined}
            aria-label="Ask a question about this document"
            className="h-full w-full bg-transparent pl-14 pr-16 text-sm tracking-[0.01em] text-on-surface outline-none placeholder:text-on-surface-variant/70"
            disabled={isThinking}
            onChange={(event) => onQuestionChange(event.target.value)}
            placeholder="Continue exploring this document..."
            value={question}
          />
          <button aria-label={isThinking ? "Waiting for an answer" : "Send query"} className="absolute right-2 flex size-10 items-center justify-center rounded-full bg-primary text-on-primary transition-colors hover:bg-primary-container focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-primary disabled:opacity-60" disabled={isThinking} type="submit">
            <ArrowUp className="size-4" strokeWidth={1.5} />
          </button>
        </form>
        <p className="mt-3 text-center text-xs text-on-surface-variant">
          Archivalist AI can make mistakes. Verify critical citations.
        </p>
        {error ? <p className="mt-3 text-center text-sm text-red-800 motion-safe:animate-[fade-in_200ms_ease-out]" id="chat-error" role="alert">{error}</p> : null}
      </div>
    </div>
  );
}
