import { FileSearch, Trash2 } from "lucide-react";
import { DocumentCard } from "@/components/upload/DocumentCard";
import type { SourceChunk, UploadedDocument } from "@/services/api";

type ContextPanelProps = {
  document: UploadedDocument;
  isDeleting: boolean;
  onDelete: () => void;
  retrievedChunks: number;
  sources: SourceChunk[];
};

export function ContextPanel({ document, isDeleting, onDelete, retrievedChunks, sources }: ContextPanelProps) {
  return (
    <aside className="hidden w-80 shrink-0 flex-col overflow-y-auto border-l bg-surface xl:flex">
      <div className="sticky top-0 border-b bg-surface/90 p-6 backdrop-blur-sm">
        <h2 className="mb-1 text-[12px] font-semibold uppercase tracking-[0.1em] text-on-surface">
          Document Intelligence
        </h2>
        <p className="text-[13px] leading-[1.4] text-on-surface-variant">Real-time analysis context</p>
      </div>

      <div className="flex flex-col gap-8 p-6">
        <section>
          <h3 className="mb-4 text-[12px] font-semibold uppercase tracking-[0.1em] text-on-surface-variant">
            Source Material
          </h3>
          <DocumentCard chunksIndexed={document.chunks_indexed} filename={document.filename} pages={document.pages} />
        </section>

        <section>
          <div className="mb-2 flex items-end justify-between">
            <h3 className="text-[12px] font-semibold uppercase tracking-[0.1em] text-on-surface-variant">
              Retrieved Chunks
            </h3>
            <span className="text-[13px] font-medium leading-[1.4] text-secondary">{retrievedChunks}</span>
          </div>
          <div className="h-1.5 overflow-hidden rounded-full bg-surface-container">
            <div className="h-full w-full rounded-full bg-secondary" />
          </div>
          <p className="mt-2 text-[11px] text-on-surface-variant">
            Sources retrieved for the most recent answer.
          </p>
        </section>

        <section>
          <h3 className="mb-4 text-[12px] font-semibold uppercase tracking-[0.1em] text-on-surface-variant">
            Reference Blocks
          </h3>
          <div className="space-y-3">
            {sources.length === 0 ? <p className="text-sm text-on-surface-variant">Ask a question to view retrieved source passages.</p> : null}
            {sources.map((source) => <ReferenceBlock key={`${source.doc_id}-${source.chunk_index}`} source={source} />)}
          </div>
        </section>

        <button aria-label="Remove uploaded document" className="flex items-center justify-center gap-2 rounded-lg border px-3 py-2 text-sm text-on-surface-variant transition-colors hover:border-outline hover:bg-surface-container-low focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-primary disabled:opacity-60" disabled={isDeleting} onClick={onDelete}>
          <Trash2 className="size-4" strokeWidth={1.5} />
          {isDeleting ? "Removing document..." : "Remove document"}
        </button>
      </div>
    </aside>
  );
}

function ReferenceBlock({ source }: { source: SourceChunk }) {
  return (
    <div className="rounded-lg border bg-surface-container-low p-3">
      <div className="flex items-start gap-2">
        <span className="mt-0.5 text-xs font-bold text-secondary">[{source.chunk_index + 1}]</span>
        <div>
          <p className="mb-2 text-sm leading-tight text-on-surface">{source.snippet}</p>
          <p className="flex items-center gap-1 text-[10px] text-on-surface-variant">
            <FileSearch className="size-3.5" strokeWidth={1.5} />
            {source.page ? `Page ${source.page}` : source.filename}
          </p>
        </div>
      </div>
    </div>
  );
}
