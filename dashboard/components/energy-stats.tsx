"use client"

import { Battery, Bolt, Lightbulb, RefreshCw, Zap } from "lucide-react"

import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import type { EnergyData } from "@/lib/data-service"

/*
  EnergyStats component for the Balkonsolar Dashboard
  - Displays solar production, battery storage, grid usage, and total consumption
  - Used in the main dashboard to show current energy statistics
*/

interface EnergyStatsProps {
  data: EnergyData
  isRefreshing?: boolean
}

export function EnergyStats({ data, isRefreshing = false }: EnergyStatsProps) {
  return (
    <Card className="relative">
      {isRefreshing && (
        <div className="absolute right-4 top-4 animate-spin text-muted-foreground">
          <RefreshCw className="h-4 w-4" />
        </div>
      )}
      <CardHeader>
        <CardTitle>Energy Statistics</CardTitle>
        <CardDescription>
          {data.timestamp.toLocaleDateString([], { month: "short", day: "numeric" })} at{" "}
          {data.timestamp.toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" })}
        </CardDescription>
      </CardHeader>
      <CardContent>
        <div className="space-y-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-2">
              <div className="rounded-full bg-yellow-100 p-1.5 text-yellow-600 dark:bg-yellow-900 dark:text-yellow-400">
                <Bolt className="h-4 w-4" />
              </div>
              <span className="text-sm font-medium">Solar Production</span>
            </div>
            <span className="font-medium">{Math.abs(data.solarProduction).toFixed(1)} kWh</span>
          </div>

          <div className="flex items-center justify-between">
            <div className="flex items-center gap-2">
              <div className="rounded-full bg-green-100 p-1.5 text-green-600 dark:bg-green-900 dark:text-green-400">
                <Battery className="h-4 w-4" />
              </div>
              <span className="text-sm font-medium">Battery Storage</span>
            </div>
            <span className="font-medium">{'85 %'}</span>
          </div>

          <div className="flex items-center justify-between">
            <div className="flex items-center gap-2">
              <div className="rounded-full bg-blue-100 p-1.5 text-blue-600 dark:bg-blue-900 dark:text-blue-400">
                <Zap className="h-4 w-4" />
              </div>
              <span className="text-sm font-medium">Grid Usage</span>
            </div>
            <span className="font-medium">{data.gridUsage.toFixed(1)} kWh</span>
          </div>

          <div className="flex items-center justify-between">
            <div className="flex items-center gap-2">
              <div className="rounded-full bg-purple-100 p-1.5 text-purple-600 dark:bg-purple-900 dark:text-purple-400">
                <Lightbulb className="h-4 w-4" />
              </div>
              <span className="text-sm font-medium">Total Consumption</span>
            </div>
            <span className="font-medium">
              {(data.output_algorithm[0]?.usage || 0).toFixed(1)} kWh
            </span>
          </div>


        </div>
      </CardContent>
    </Card>
  )
}
