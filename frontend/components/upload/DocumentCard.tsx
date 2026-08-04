import { CheckCircle2, FileText } from "lucide-react";

type DocumentCardProps = {
  filename: string;
  pages: number;
  chunksIndexed: number;
};

export function DocumentCard({ filename, pages, chunksIndexed }: DocumentCardProps) {
  return (
    <article className="overflow-hidden rounded-xl border bg-surface-container-lowest shadow-[0_8px_30px_rgb(0,0,0,0.04)] transition-all duration-300 hover:border-outline hover:shadow-[0_8px_30px_rgb(0,0,0,0.06)]">
      <div className="relative h-32 bg-surface-container [background-image:radial-gradient(#181916_1px,transparent_1px)] [background-size:12px_12px]">
        <span className="absolute bottom-3 left-3 rounded bg-surface px-2 py-1 text-[10px] font-bold tracking-wider text-on-surface shadow-sm">
          PDF
        </span>
      </div>
      <div className="p-4">
        <div className="flex items-start gap-3">
          <FileText className="mt-0.5 size-5 shrink-0 text-secondary" strokeWidth={1.5} />
          <div className="min-w-0">
            <h3 className="truncate text-sm font-medium text-on-surface">{filename}</h3>
            <p className="mt-1 text-[13px] leading-[1.4] text-on-surface-variant">
              {pages} pages · {chunksIndexed} chunks indexed
            </p>
          </div>
          <CheckCircle2 className="size-5 shrink-0 text-secondary" strokeWidth={1.5} />
        </div>
      </div>
    </article>
  );
}
