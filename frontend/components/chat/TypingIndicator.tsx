export function TypingIndicator() {
  return (
    <div className="flex items-center gap-2 text-[13px] leading-[1.4] text-on-surface-variant motion-safe:animate-[fade-in_200ms_ease-out]" aria-label="Archivalist AI is preparing a response" role="status">
      <span>Reviewing source passages</span>
      <span className="flex gap-1" aria-hidden="true">
        <i className="size-1.5 rounded-full bg-secondary motion-safe:animate-pulse [animation-delay:-0.3s]" />
        <i className="size-1.5 rounded-full bg-secondary motion-safe:animate-pulse [animation-delay:-0.15s]" />
        <i className="size-1.5 rounded-full bg-secondary motion-safe:animate-pulse" />
      </span>
    </div>
  );
}
