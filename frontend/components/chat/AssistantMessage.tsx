import type { ReactNode } from "react";

type AssistantMessageProps = {
  title?: string;
  answer?: string;
  children?: ReactNode;
};

export function AssistantMessage({ title, answer, children }: AssistantMessageProps) {
  return (
    <article className="w-full">
      <span className="mb-6 inline-block rounded-full border bg-surface-container px-3 py-1 text-[12px] font-semibold uppercase tracking-[0.1em] text-on-surface-variant">
        Research synthesis
      </span>
      {title ? <h1 className="mb-6 text-4xl font-semibold leading-[1.1] tracking-[-0.03em] text-primary md:text-5xl">{title}</h1> : null}
      <div className="space-y-8 text-lg leading-[1.7] text-on-surface">
        {answer
          ? answer.split(/\n{2,}/).map((paragraph, index) => (
              <p className="whitespace-pre-wrap" key={`${paragraph}-${index}`}>{paragraph}</p>
            ))
          : children}
      </div>
    </article>
  );
}
