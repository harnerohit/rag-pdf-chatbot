import { FileText, FolderArchive, Settings } from "lucide-react";
import { UnavailableTooltip } from "@/components/ui/UnavailableTooltip";

export function Sidebar() {
  return (
    <aside className="fixed inset-y-0 left-0 z-50 hidden w-64 flex-col border-r bg-surface py-16 md:flex">
      <div className="flex items-center gap-4 px-6">
        <div className="flex size-10 items-center justify-center rounded-full border bg-primary text-xs font-semibold tracking-[0.1em] text-on-primary shadow-sm">
          AA
        </div>
        <div>
          <h1 className="text-xl font-medium tracking-tight text-primary">Archivalist AI</h1>
          <p className="text-[13px] leading-[1.4] text-on-surface-variant">Premium Workspace</p>
        </div>
      </div>

      <nav aria-label="Workspace navigation" className="mt-16 flex flex-col gap-2">
        <span className="mr-4 flex items-center gap-3 rounded-r-full border-l-2 border-primary bg-surface-container-low py-3 pl-4 font-bold text-primary">
          <FileText className="size-5 fill-current" strokeWidth={1.5} />
          Documents
        </span>
        <UnavailableTooltip className="block" message="Coming Soon">
          <button aria-disabled="true" aria-label="Collections. Coming Soon" className="flex w-full cursor-not-allowed items-center gap-3 py-3 pl-4 text-left text-on-surface-variant opacity-55" disabled tabIndex={-1} type="button">
            <FolderArchive className="size-5" strokeWidth={1.5} />
            Collections
          </button>
        </UnavailableTooltip>
        <UnavailableTooltip className="block" message="Coming Soon">
          <button aria-disabled="true" aria-label="Settings. Coming Soon" className="flex w-full cursor-not-allowed items-center gap-3 py-3 pl-4 text-left text-on-surface-variant opacity-55" disabled tabIndex={-1} type="button">
            <Settings className="size-5" strokeWidth={1.5} />
            Settings
          </button>
        </UnavailableTooltip>
      </nav>

      <div className="mt-auto px-6">
        <UnavailableTooltip className="block" message="Storage management will be available in a future update." tooltipClassName="top-auto bottom-full mt-0 mb-2">
          <div aria-disabled="true" aria-label="Workspace Quota. Storage management will be available in a future update." className="cursor-not-allowed rounded-lg border bg-surface-container p-4 opacity-55">
            <p className="mb-2 text-[12px] font-semibold uppercase tracking-[0.1em] text-on-surface-variant">
              Workspace Quota
            </p>
            <div className="h-1 overflow-hidden rounded-full bg-surface">
              <div className="h-full w-[45%] rounded-full bg-secondary" />
            </div>
            <p className="mt-2 text-right text-[13px] leading-[1.4] text-on-surface-variant">4.5 GB / 10 GB</p>
          </div>
        </UnavailableTooltip>
      </div>
    </aside>
  );
}
