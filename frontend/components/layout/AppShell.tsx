import { Menu } from "lucide-react";
import type { ReactNode } from "react";
import { Sidebar } from "@/components/layout/Sidebar";
import { Workspace } from "@/components/layout/Workspace";

type AppShellProps = {
  children?: ReactNode;
  contextPanel?: ReactNode;
};

export function AppShell({ children, contextPanel }: AppShellProps) {
  return (
    <div className="min-h-screen bg-surface text-on-surface md:h-screen md:overflow-hidden">
      <Sidebar />

      <div className="min-h-screen md:ml-64 md:h-screen">
        <header className="flex h-20 items-center justify-between border-b bg-surface px-6 md:hidden">
          <div className="flex items-center gap-2">
            <div className="flex size-8 items-center justify-center rounded-full bg-primary text-[10px] font-semibold tracking-[0.1em] text-on-primary">
              AA
            </div>
            <h1 className="text-[28px] font-medium leading-[1.2] tracking-[-0.02em] text-primary">
              Archivalist AI
            </h1>
          </div>
          <button aria-label="Menu" className="p-2 text-on-surface-variant" disabled>
            <Menu className="size-5" strokeWidth={1.5} />
          </button>
        </header>

        <div className="flex min-h-[calc(100vh-5rem)] md:h-screen md:min-h-0">
          {children ?? <Workspace />}
          {contextPanel}
        </div>
      </div>
    </div>
  );
}
