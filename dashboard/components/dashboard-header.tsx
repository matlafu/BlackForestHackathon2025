"use client"

import { useState } from "react"
import { Battery, Menu, Settings, Sun, ToggleLeft } from "lucide-react"

import { Button } from "@/components/ui/button"
import { ControlCenterDialog } from "@/components/control-center"
import { ModeToggle } from "@/components/mode-toggle"
import { SettingsModal } from "@/components/settings-modal"
import type { EnergyData } from "@/lib/data-service"

interface DashboardHeaderProps {
  mode: "realtime" | "historic"
  setMode: (mode: "realtime" | "historic") => void
  data: EnergyData | null
  isRefreshing?: boolean
}

export function DashboardHeader({ mode, setMode, data, isRefreshing = false }: DashboardHeaderProps) {
  const [settingsOpen, setSettingsOpen] = useState(false)
  const [controlCenterOpen, setControlCenterOpen] = useState(false)

  return (
    <header className="sticky top-0 z-10 border-b bg-background/95 backdrop-blur">
      <div className="flex h-16 items-center px-6">
        <Button variant="ghost" size="icon" className="mr-2 md:hidden">
          <Menu className="h-5 w-5" />
          <span className="sr-only">Toggle menu</span>
        </Button>
        <div className="flex items-center gap-2">
          <Sun className="h-6 w-6 text-yellow-500" />
          <h1 className="text-lg font-semibold">BalkonSolar Dashboard</h1>
        </div>
        <div className="ml-auto flex items-center gap-4">
          <div className="flex items-center gap-2">
            <Battery className="h-5 w-5 text-green-500" />
            <span className="font-medium">85%</span>
          </div>
          <ModeToggle mode={mode} setMode={setMode} />
          <Button size="sm" variant="outline" onClick={() => setControlCenterOpen(true)}>
            <ToggleLeft className="h-4 w-4 mr-2" />
            Control Center
          </Button>
          <Button size="sm" onClick={() => setSettingsOpen(true)}>
            <Settings className="h-4 w-4 mr-2" />
            Settings
          </Button>
        </div>
      </div>

      <SettingsModal open={settingsOpen} onOpenChange={setSettingsOpen} />
      {data && (
        <ControlCenterDialog
          open={controlCenterOpen}
          onOpenChange={setControlCenterOpen}
          data={data}
          isRefreshing={isRefreshing}
        />
      )}
    </header>
  )
}
