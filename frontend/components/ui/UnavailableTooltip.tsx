import type { ReactNode } from "react";
import { cn } from "@/lib/utils";

type UnavailableTooltipProps = {
  children: ReactNode;
  message: string;
  className?: string;
  tooltipClassName?: string;
};

export function UnavailableTooltip({ children, message, className, tooltipClassName }: UnavailableTooltipProps) {
  return (
    <span className={cn("group relative inline-flex", className)}>
      {children}
      <span className={cn("pointer-events-none invisible absolute left-1/2 top-full z-10 mt-2 w-max max-w-56 -translate-x-1/2 rounded-lg bg-primary px-3 py-2 text-center text-[11px] font-medium leading-[1.4] tracking-[0.01em] text-on-primary opacity-0 shadow-[0_8px_24px_rgb(0,0,0,0.12)] group-hover:visible group-hover:opacity-100", tooltipClassName)} role="tooltip">
        {message}
      </span>
    </span>
  );
}
