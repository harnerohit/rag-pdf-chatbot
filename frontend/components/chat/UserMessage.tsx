type UserMessageProps = {
  children: string;
};

export function UserMessage({ children }: UserMessageProps) {
  return (
    <section className="ml-auto max-w-xl rounded-xl border bg-surface-container-low p-5">
      <p className="mb-2 text-[12px] font-semibold uppercase tracking-[0.1em] text-on-surface-variant">You</p>
      <p className="text-base leading-[1.7] text-on-surface">{children}</p>
    </section>
  );
}
