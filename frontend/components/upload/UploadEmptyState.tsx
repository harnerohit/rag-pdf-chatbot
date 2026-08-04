"use client";

import { Download, LoaderCircle, MoreVertical, Share2, Upload } from "lucide-react";
import { UnavailableTooltip } from "@/components/ui/UnavailableTooltip";

type UploadEmptyStateProps = {
  onFileSelect: (file: File) => void;
  isUploading: boolean;
  error: string | null;
};

export function UploadEmptyState({ onFileSelect, isUploading, error }: UploadEmptyStateProps) {
  return (
    <main aria-busy={isUploading} className="relative flex min-w-0 flex-1 flex-col overflow-y-auto bg-surface motion-safe:animate-[fade-in_300ms_ease-out]">
      <div className="absolute right-0 top-0 hidden h-20 items-center gap-4 px-16 text-on-surface-variant md:flex">
        <UnavailableTooltip message="Available in a future update">
          <button aria-disabled="true" aria-label="Share. Available in a future update" className="cursor-not-allowed rounded-lg p-2 opacity-55" disabled tabIndex={-1} type="button">
            <Share2 className="size-5" strokeWidth={1.5} />
          </button>
        </UnavailableTooltip>
        <UnavailableTooltip message="Available in a future update">
          <button aria-disabled="true" aria-label="Download. Available in a future update" className="cursor-not-allowed rounded-lg p-2 opacity-55" disabled tabIndex={-1} type="button">
            <Download className="size-5" strokeWidth={1.5} />
          </button>
        </UnavailableTooltip>
        <UnavailableTooltip message="Available in a future update">
          <button aria-disabled="true" aria-label="More options. Available in a future update" className="cursor-not-allowed rounded-lg p-2 opacity-55" disabled tabIndex={-1} type="button">
            <MoreVertical className="size-5" strokeWidth={1.5} />
          </button>
        </UnavailableTooltip>
      </div>

      <div className="flex flex-1 flex-col items-center justify-center px-6 py-[120px] md:px-16">
        <div className="mb-16 max-w-3xl text-center">
          <h2 className="mb-6 text-4xl font-semibold leading-[1.1] tracking-[-0.04em] text-primary sm:text-5xl md:text-[64px]">
            A place where documents become conversations.
          </h2>
          <p className="mx-auto max-w-xl text-lg leading-[1.7] text-on-surface-variant">
            Upload your research materials to begin extracting insights, tracing citations, and conversing with your archives.
          </p>
        </div>

        <div className="w-full max-w-2xl">
          <div className="group relative flex min-h-[355px] flex-col items-center justify-center rounded-xl border bg-surface-container-lowest p-10 text-center shadow-[0_16px_32px_rgba(24,25,22,0.03)] transition-all duration-300 hover:-translate-y-0.5 hover:border-primary hover:shadow-[0_16px_32px_rgba(24,25,22,0.06)] focus-within:border-primary focus-within:ring-2 focus-within:ring-primary/15 md:p-16">
            <div className="pointer-events-none absolute inset-2 rounded-lg border-2 border-dashed border-transparent transition-colors duration-300 group-hover:border-outline-variant/30" />
            <div className="mb-6 flex size-20 items-center justify-center rounded-full bg-surface-container-low text-on-surface-variant">
              {isUploading ? <LoaderCircle className="size-10 motion-safe:animate-spin" strokeWidth={1.5} /> : <Upload className="size-10" strokeWidth={1.5} />}
            </div>
            <h3 className="mb-2 text-[32px] font-medium leading-[1.2] tracking-[-0.02em] text-primary">
              Select files or drag and drop
            </h3>
            <p className="mb-8 text-sm leading-[1.5] tracking-[0.01em] text-on-surface-variant">
              Your private workspace awaits.
            </p>
            <label
              className="cursor-pointer rounded bg-primary px-6 py-3 text-sm leading-[1.5] tracking-[0.01em] text-on-primary transition-colors duration-200 hover:bg-primary-container focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-4 focus-visible:outline-primary"
              htmlFor="pdf-upload"
            >
              {isUploading ? "Uploading PDF..." : "Browse Files"}
              <input
                accept=".pdf,application/pdf"
                className="sr-only"
                disabled={isUploading}
                id="pdf-upload"
                onChange={(event) => {
                  const file = event.target.files?.[0];
                  if (file) onFileSelect(file);
                  event.target.value = "";
                }}
                type="file"
              />
            </label>
          </div>

          <p className="mt-8 text-center text-[13px] leading-[1.4] text-on-surface-variant/70">
            Supported format: PDF.
          </p>
          {isUploading ? <p className="mt-3 text-center text-sm text-on-surface-variant" role="status">Indexing your PDF…</p> : null}
          {error ? <p className="mt-3 text-center text-sm text-red-800 motion-safe:animate-[fade-in_200ms_ease-out]" role="alert">{error}</p> : null}
        </div>
      </div>
    </main>
  );
}
