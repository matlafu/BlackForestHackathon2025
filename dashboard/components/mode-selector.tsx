"use client"

import { Clock, History } from "lucide-react"

import { Card, CardContent } from "@/components/ui/card"
import { Tabs, TabsList, TabsTrigger } from "@/components/ui/tabs"

interface ModeSelectorProps {
  mode: "realtime" | "historic"
  setMode: (mode: "realtime" | "historic") => void
}

export function ModeSelector({ mode, setMode }: ModeSelectorProps) {
  return (
    <Card>
      <CardContent className="pt-6">
        <div className="flex flex-col space-y-4">
          <Tabs value={mode} onValueChange={(value) => setMode(value as "realtime" | "historic")} className="w-full">
            <TabsList className="grid w-full grid-cols-2">
              <TabsTrigger value="realtime" className="flex items-center gap-2">
                <Clock className="h-4 w-4" />
                <span>Realtime</span>
              </TabsTrigger>
              <TabsTrigger value="historic" className="flex items-center gap-2">
                <History className="h-4 w-4" />
                <span>Historic</span>
              </TabsTrigger>
            </TabsList>
          </Tabs>

          {mode === "realtime" && (
            <div className="flex items-center justify-between">
              <div className="flex items-center gap-2">
                <div className="h-2 w-2 animate-pulse rounded-full bg-green-500"></div>
                <span className="text-sm text-muted-foreground">Live data</span>
              </div>
              <span className="text-sm font-medium">
                {new Date().toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" })}
              </span>
            </div>
          )}

          {mode === "historic" && (
            <div className="flex items-center justify-between">
              <span className="text-sm text-muted-foreground">Select a time on the graph below</span>
              <span className="text-xs text-muted-foreground">Last 24 hours</span>
            </div>
          )}
        </div>
      </CardContent>
    </Card>
  )
}
