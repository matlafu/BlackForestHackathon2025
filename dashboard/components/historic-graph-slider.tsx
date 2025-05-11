"use client"

import type React from "react"

import { useEffect, useRef, useState } from "react"
import { Battery, ChevronLeft, ChevronRight, Clock } from "lucide-react"

import { Card, CardContent } from "@/components/ui/card"
import { Tooltip, TooltipContent, TooltipProvider, TooltipTrigger } from "@/components/ui/tooltip"
import { generateHistoricBatteryData } from "@/lib/data-service"

interface HistoricGraphSliderProps {
  mode: "realtime" | "historic"
  selectedTime: Date
  setSelectedTime: (time: Date) => void
}

export function HistoricGraphSlider({ mode, selectedTime, setSelectedTime }: HistoricGraphSliderProps) {
  const [batteryData, setBatteryData] = useState<{ time: Date; level: number }[]>([])
  const [isDragging, setIsDragging] = useState(false)
  const sliderRef = useRef<HTMLDivElement>(null)
  const isRealtime = mode === "realtime"

  // Generate 24 hours of battery data
  useEffect(() => {
    setBatteryData(generateHistoricBatteryData())
  }, [])

  // Find the closest data point to the selected time
  const selectedIndex = batteryData.findIndex(
    (data) => data.time.getHours() === selectedTime.getHours() && data.time.getDate() === selectedTime.getDate(),
  )

  // Handle click on the graph to select a time
  const handleGraphClick = (e: React.MouseEvent<HTMLDivElement>) => {
    if (isRealtime || !sliderRef.current || batteryData.length === 0) return

    const rect = sliderRef.current.getBoundingClientRect()
    const x = e.clientX - rect.left
    const width = rect.width
    const index = Math.min(Math.floor((x / width) * batteryData.length), batteryData.length - 1)

    setSelectedTime(new Date(batteryData[index].time))
  }

  // Handle mouse move for dragging
  const handleMouseMove = (e: MouseEvent) => {
    if (isRealtime || !isDragging || !sliderRef.current || batteryData.length === 0) return

    const rect = sliderRef.current.getBoundingClientRect()
    const x = e.clientX - rect.left
    const width = rect.width
    const index = Math.min(Math.max(0, Math.floor((x / width) * batteryData.length)), batteryData.length - 1)

    setSelectedTime(new Date(batteryData[index].time))
  }

  // Set up and clean up event listeners for dragging
  useEffect(() => {
    if (isDragging && !isRealtime) {
      window.addEventListener("mousemove", handleMouseMove)
      window.addEventListener("mouseup", () => setIsDragging(false))
    }

    return () => {
      window.removeEventListener("mousemove", handleMouseMove)
      window.removeEventListener("mouseup", () => setIsDragging(false))
    }
  }, [isDragging, isRealtime])

  // Move to previous or next hour
  const moveTime = (direction: -1 | 1) => {
    if (isRealtime || batteryData.length === 0) return

    const currentIndex = batteryData.findIndex(
      (data) => data.time.getHours() === selectedTime.getHours() && data.time.getDate() === selectedTime.getDate(),
    )

    if (currentIndex === -1) return

    const newIndex = Math.max(0, Math.min(batteryData.length - 1, currentIndex + direction))
    setSelectedTime(new Date(batteryData[newIndex].time))
  }

  return (
    <Card className={isRealtime ? "opacity-70" : ""}>
      <CardContent className="pt-6">
        <div className="space-y-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-2">
              <Battery className="h-5 w-5 text-green-500" />
              <span className="font-medium">Battery History (Last 24h)</span>
            </div>
            <div className="flex items-center gap-2">
              {isRealtime ? (
                <div className="flex items-center gap-2 text-sm text-muted-foreground">
                  <Clock className="h-4 w-4" />
                  <span>Realtime mode</span>
                </div>
              ) : (
                <>
                  <button
                    onClick={() => moveTime(-1)}
                    className="rounded-full p-1 hover:bg-muted disabled:opacity-50"
                    disabled={isRealtime || selectedIndex <= 0}
                  >
                    <ChevronLeft className="h-4 w-4" />
                  </button>
                  <span className="text-sm font-medium">
                    {selectedTime.toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" })}
                    {" - "}
                    {selectedTime.toLocaleDateString([], { month: "short", day: "numeric" })}
                  </span>
                  <button
                    onClick={() => moveTime(1)}
                    className="rounded-full p-1 hover:bg-muted disabled:opacity-50"
                    disabled={isRealtime || selectedIndex >= batteryData.length - 1}
                  >
                    <ChevronRight className="h-4 w-4" />
                  </button>
                </>
              )}
            </div>
          </div>

          {/* Battery level graph */}
          <div
            ref={sliderRef}
            className={`relative h-24 w-full rounded-md bg-muted ${isRealtime ? "cursor-not-allowed" : "cursor-pointer"}`}
            onClick={handleGraphClick}
            onMouseDown={() => !isRealtime && setIsDragging(true)}
          >
            {/* Graph bars */}
            <div className="flex h-full w-full items-end">
              {batteryData.map((data, i) => (
                <TooltipProvider key={i}>
                  <Tooltip>
                    <TooltipTrigger asChild>
                      <div
                        className={`relative flex-1 transition-all ${
                          i === selectedIndex ? "bg-green-500" : "bg-green-300"
                        }`}
                        style={{ height: `${data.level * 100}%` }}
                      >
                        {i === selectedIndex && (
                          <div className="absolute -top-2 left-1/2 h-4 w-4 -translate-x-1/2 transform rounded-full bg-green-500 ring-2 ring-background" />
                        )}
                      </div>
                    </TooltipTrigger>
                    <TooltipContent>
                      <div className="text-xs">
                        <div>{data.time.toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" })}</div>
                        <div className="font-bold">{Math.round(data.level * 100)}% charged</div>
                      </div>
                    </TooltipContent>
                  </Tooltip>
                </TooltipProvider>
              ))}
            </div>

            {/* Time labels */}
            <div className="absolute bottom-0 left-0 right-0 flex justify-between px-2 text-xs text-muted-foreground">
              {[0, 6, 12, 18, 23].map((hour) => (
                <div key={hour}>{batteryData[hour]?.time.getHours()}:00</div>
              ))}
            </div>

            {/* Realtime mode overlay */}
            {isRealtime && (
              <div className="absolute inset-0 flex items-center justify-center bg-background/30 backdrop-blur-[1px]">
                <div className="rounded-md bg-background/80 px-3 py-1.5 text-xs font-medium">
                  Switch to historic mode to select time
                </div>
              </div>
            )}
          </div>

          {/* Battery level indicator */}
          <div className="flex items-center justify-between">
            <span className="text-xs text-muted-foreground">0%</span>
            <div className="mx-2 h-2 flex-1 overflow-hidden rounded-full bg-muted">
              <div
                className="h-full rounded-full bg-green-500"
                style={{ width: `${batteryData[selectedIndex]?.level * 100 || 0}%` }}
              />
            </div>
            <span className="text-xs text-muted-foreground">100%</span>
          </div>
        </div>
      </CardContent>
    </Card>
  )
}
