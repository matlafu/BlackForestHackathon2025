"use client"

import { Clock, History } from "lucide-react"

import { Toggle } from "@/components/ui/toggle"
import { Tooltip, TooltipContent, TooltipProvider, TooltipTrigger } from "@/components/ui/tooltip"

interface ModeToggleProps {
  mode: "realtime" | "historic"
  setMode: (mode: "realtime" | "historic") => void
}

export function ModeToggle({ mode, setMode }: ModeToggleProps) {
  return (
    <div className="flex items-center gap-2">
      {mode === "realtime" && (
        <div className="flex items-center gap-1.5">
          <div className="h-1.5 w-1.5 animate-pulse rounded-full bg-green-500"></div>
          <span className="text-xs text-muted-foreground">Live</span>
        </div>
      )}

      <TooltipProvider>
        <Tooltip>
          <TooltipTrigger asChild>
            <Toggle
              variant="outline"
              size="sm"
              pressed={mode === "historic"}
              onPressedChange={(pressed) => setMode(pressed ? "historic" : "realtime")}
              aria-label="Toggle historic mode"
            >
              {mode === "realtime" ? <Clock className="h-3.5 w-3.5" /> : <History className="h-3.5 w-3.5" />}
            </Toggle>
          </TooltipTrigger>
          <TooltipContent side="bottom">
            <p>{mode === "realtime" ? "Switch to historic mode" : "Switch to realtime mode"}</p>
          </TooltipContent>
        </Tooltip>
      </TooltipProvider>
    </div>
  )
}
