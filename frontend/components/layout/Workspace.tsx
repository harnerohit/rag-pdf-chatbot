import { ArrowUp, Lightbulb, MoreVertical, Paperclip, Share2, Download } from "lucide-react";
import { UnavailableTooltip } from "@/components/ui/UnavailableTooltip";

export function Workspace() {
  return (
    <main className="relative flex min-w-0 flex-1 flex-col bg-surface">
      <header className="hidden h-16 items-center justify-between border-b bg-surface/80 px-16 backdrop-blur-md md:flex">
        <div className="flex items-center gap-4 text-[13px] leading-[1.4] text-on-surface-variant">
          <span>
            Project: <strong className="font-semibold text-on-surface">Neural Architecture</strong>
          </span>
          <span className="size-1 rounded-full bg-outline-variant" />
          <span>Last analyzed 2 mins ago</span>
        </div>
        <div className="flex items-center gap-1">
          <ActionButton label="Share"><Share2 /></ActionButton>
          <ActionButton label="Download"><Download /></ActionButton>
          <ActionButton label="More options"><MoreVertical /></ActionButton>
        </div>
      </header>

      <div className="flex min-h-0 flex-1 overflow-y-auto px-6 py-12 pb-40 md:px-16">
        <article className="mx-auto w-full max-w-3xl">
          <header className="mb-16">
            <span className="mb-6 inline-block rounded-full border bg-surface-container px-3 py-1 text-[12px] font-semibold uppercase tracking-[0.1em] text-on-surface-variant">
              Synthesis Report
            </span>
            <h2 className="mb-6 text-4xl font-semibold leading-[1.1] tracking-[-0.03em] text-primary md:text-5xl">
              Evolution of Attention Mechanisms in Transformer Models
            </h2>
            <p className="text-lg leading-[1.7] text-on-surface-variant">
              A comprehensive analysis of multi-head attention evolution from the seminal ‘Attention is All You Need’ paper to modern sparse attention paradigms.
            </p>
          </header>

          <div className="space-y-8 text-lg leading-[1.7] text-on-surface">
            <p>
              The fundamental shift in natural language processing was catalyzed by the introduction of the self-attention mechanism, which allowed models to weigh the importance of different words in a sequence regardless of their positional distance. Unlike recurrent architectures, this approach enabled massive parallelization during training.
              <sup className="ml-1 cursor-default text-secondary">[1]</sup>
            </p>

            <section className="relative my-10 rounded-r-xl border-l-4 border-secondary bg-surface-container-low p-8 shadow-[0_8px_30px_rgb(0,0,0,0.04)]">
              <Lightbulb className="absolute right-6 top-6 size-9 text-outline-variant/50" strokeWidth={1.5} />
              <h3 className="mb-3 text-xl font-medium tracking-[-0.02em] text-primary">Key Insight</h3>
              <p>
                The transition from dense to sparse attention models reduced memory complexity from <strong>O(n²)</strong> to <strong>O(n log n)</strong>, unlocking the ability to process document-level contexts previously impossible for standard transformers.
              </p>
            </section>

            <section>
              <h3 className="mb-6 mt-12 text-[32px] font-medium leading-[1.2] tracking-[-0.02em] text-primary">
                Comparative Architecture Analysis
              </h3>
              <p className="mb-6">
                Analyzing the structural differences between dominant architectures reveals a trade-off between expressive capability and computational efficiency. The table below synthesizes findings across three key structural paradigms.
              </p>
              <div className="my-8 overflow-x-auto rounded-xl border">
                <table className="w-full min-w-[640px] border-collapse text-left text-sm">
                  <thead className="border-b bg-surface-container text-[12px] uppercase tracking-[0.1em] text-on-surface">
                    <tr>
                      <th className="p-4 font-semibold">Architecture</th>
                      <th className="p-4 font-semibold">Complexity</th>
                      <th className="p-4 font-semibold">Context Window</th>
                      <th className="p-4 font-semibold">Primary Trade-off</th>
                    </tr>
                  </thead>
                  <tbody className="text-on-surface-variant">
                    <TableRow architecture="Standard Transformer" complexity="O(N²)" context="4k – 8k tokens" tradeOff="Quadratic scaling limits" />
                    <TableRow architecture="Reformer (LSH)" complexity="O(N log N)" context="64k tokens" tradeOff="Hash collision artifacts" />
                    <TableRow architecture="Longformer" complexity="O(N × W)" context="100k+ tokens" tradeOff="Local context bias" />
                  </tbody>
                </table>
              </div>
            </section>

            <section>
              <h3 className="mb-6 mt-12 text-[32px] font-medium leading-[1.2] tracking-[-0.02em] text-primary">
                Future Directions in Sparse Representation
              </h3>
              <p>
                Recent methodologies suggest that dynamic sparsity, where the model learns which tokens to attend to during inference rather than relying on fixed patterns, offers the most promising path toward universal context processing. Models leveraging routing networks to dictate attention flow show significant improvements in both perplexity and zero-shot reasoning tasks on long-form documents.
                <sup className="ml-1 cursor-default text-secondary">[2]</sup>
              </p>
            </section>
          </div>
        </article>
      </div>

      <div className="pointer-events-none absolute inset-x-0 bottom-0 bg-gradient-to-t from-surface via-surface to-transparent px-6 pb-6 pt-12 md:px-16">
        <div className="pointer-events-auto mx-auto max-w-3xl">
          <div className="relative flex h-14 items-center rounded-full border bg-surface shadow-[0_8px_30px_rgb(0,0,0,0.06)]">
            <button aria-label="Attach file" className="absolute left-2 flex size-10 items-center justify-center rounded-full text-on-surface-variant" disabled>
              <Paperclip className="size-5" strokeWidth={1.5} />
            </button>
            <span className="pl-14 text-sm text-on-surface-variant/70">Continue exploring this document...</span>
            <button aria-label="Send query" className="absolute right-2 flex size-10 items-center justify-center rounded-full bg-primary text-on-primary" disabled>
              <ArrowUp className="size-4" strokeWidth={1.5} />
            </button>
          </div>
          <p className="mt-3 text-center text-xs text-on-surface-variant">
            Archivalist AI can make mistakes. Verify critical citations.
          </p>
        </div>
      </div>
    </main>
  );
}

function ActionButton({ children, label }: { children: React.ReactNode; label: string }) {
  return (
    <UnavailableTooltip message="Available in a future update">
      <button aria-disabled="true" aria-label={`${label}. Available in a future update`} className="cursor-not-allowed rounded-lg p-2 text-on-surface-variant opacity-55" disabled tabIndex={-1} type="button">
        {children}
      </button>
    </UnavailableTooltip>
  );
}

function TableRow({ architecture, complexity, context, tradeOff }: { architecture: string; complexity: string; context: string; tradeOff: string }) {
  return (
    <tr className="border-b last:border-0">
      <td className="p-4 font-medium text-on-surface">{architecture}</td>
      <td className="p-4">{complexity}</td>
      <td className="p-4">{context}</td>
      <td className="p-4">{tradeOff}</td>
    </tr>
  );
}
