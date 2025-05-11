"use client"

import { useState, useEffect } from "react"
import { Battery, Home, Power, Sun, Cloud, Moon } from "lucide-react"
import { Button } from "@/components/ui/button"
import { Switch } from "@/components/ui/switch"
import { Label } from "@/components/ui/label"
import { Slider } from "@/components/ui/slider"
import { Card, CardContent } from "@/components/ui/card"
import { Progress } from "@/components/ui/progress"

export default function EnergyFlowVisual() {
  const [timeOfDay, setTimeOfDay] = useState("day")
  const [weather, setWeather] = useState("sunny")
  const [solarActive, setSolarActive] = useState(true)
  const [gridActive, setGridActive] = useState(true)
  const [solarOutput, setSolarOutput] = useState(75)
  const [consumption, setConsumption] = useState(50)
  const [batteryLevel, setBatteryLevel] = useState(60)
  const [batteryCharging, setBatteryCharging] = useState(true)

  // Update solar output based on time and weather
  useEffect(() => {
    if (timeOfDay === "night") {
      setSolarOutput(weather === "sunny" ? 10 : 5)
    } else {
      setSolarOutput(weather === "sunny" ? 75 : 40)
    }
  }, [timeOfDay, weather])

  // Calculate energy flows
  const solarToHome = solarActive ? Math.min(solarOutput, consumption) : 0
  const solarToBattery = solarActive ? Math.max(0, solarOutput - consumption) : 0
  const batteryToHome = Math.max(0, consumption - solarToHome)
  const gridToHome = gridActive ? Math.max(0, consumption - solarToHome - (batteryLevel > 10 ? batteryToHome : 0)) : 0
  const solarToGrid = solarActive && gridActive ? Math.max(0, solarOutput - consumption - solarToBattery) : 0

  // Update battery status
  useEffect(() => {
    const charging = solarToBattery > 0
    setBatteryCharging(charging)

    // Simulate battery level changes
    const interval = setInterval(() => {
      setBatteryLevel((prev) => {
        if (charging && prev < 100) {
          return Math.min(100, prev + 1)
        } else if (!charging && batteryToHome > 0 && prev > 0) {
          return Math.max(0, prev - 1)
        }
        return prev
      })
    }, 3000)

    return () => clearInterval(interval)
  }, [solarToBattery, batteryToHome])

  // Get flow intensity class
  const getFlowIntensity = (value: number) => {
    if (value === 0) return "opacity-0"
    if (value < 25) return "opacity-40"
    if (value < 50) return "opacity-60"
    if (value < 75) return "opacity-80"
    return "opacity-100"
  }

  // Get flow animation speed
  const getAnimationSpeed = (value: number) => {
    if (value === 0) return "animation-duration-0"
    if (value < 25) return "animation-duration-[8s]"
    if (value < 50) return "animation-duration-[5s]"
    if (value < 75) return "animation-duration-[3s]"
    return "animation-duration-[2s]"
  }

  return (
    <Card className="overflow-hidden">
      <CardContent className="p-0">
        <div className="relative h-[500px] bg-gradient-to-b from-sky-50 to-white dark:from-slate-900 dark:to-slate-800 p-6">
          {/* Controls */}
          <div className="absolute top-4 left-4 right-4 z-20 flex flex-wrap gap-2 justify-between">
            <div className="flex gap-2">
              <Button
                size="sm"
                variant={timeOfDay === "day" ? "default" : "outline"}
                onClick={() => setTimeOfDay("day")}
                className="rounded-full w-10 h-10 p-0"
              >
                <Sun size={18} />
              </Button>
              <Button
                size="sm"
                variant={timeOfDay === "night" ? "default" : "outline"}
                onClick={() => setTimeOfDay("night")}
                className="rounded-full w-10 h-10 p-0"
              >
                <Moon size={18} />
              </Button>
              <Button
                size="sm"
                variant={weather === "sunny" ? "default" : "outline"}
                onClick={() => setWeather("sunny")}
                className="rounded-full w-10 h-10 p-0"
              >
                <Sun size={18} />
              </Button>
              <Button
                size="sm"
                variant={weather === "cloudy" ? "default" : "outline"}
                onClick={() => setWeather("cloudy")}
                className="rounded-full w-10 h-10 p-0"
              >
                <Cloud size={18} />
              </Button>
            </div>
            <div className="flex gap-4">
              <div className="flex items-center gap-2">
                <Switch checked={solarActive} onCheckedChange={setSolarActive} id="solar-switch" />
                <Label htmlFor="solar-switch" className="text-sm">
                  Solar
                </Label>
              </div>
              <div className="flex items-center gap-2">
                <Switch checked={gridActive} onCheckedChange={setGridActive} id="grid-switch" />
                <Label htmlFor="grid-switch" className="text-sm">
                  Netz
                </Label>
              </div>
            </div>
          </div>

          {/* Sky background with sun/moon */}
          <div className="absolute inset-0 overflow-hidden">
            {timeOfDay === "day" ? (
              <div className="absolute top-6 right-12 w-16 h-16 rounded-full bg-yellow-300 shadow-[0_0_40px_20px_rgba(250,204,21,0.4)]"></div>
            ) : (
              <div className="absolute top-6 right-12 w-12 h-12 rounded-full bg-slate-200 shadow-[0_0_30px_15px_rgba(226,232,240,0.2)]"></div>
            )}

            {weather === "cloudy" && (
              <>
                <div className="absolute top-10 left-1/4 w-20 h-8 rounded-full bg-white/80 dark:bg-white/20 blur-sm"></div>
                <div className="absolute top-14 left-1/4 translate-x-6 w-24 h-8 rounded-full bg-white/80 dark:bg-white/20 blur-sm"></div>
                <div className="absolute top-8 right-1/3 w-28 h-10 rounded-full bg-white/80 dark:bg-white/20 blur-sm"></div>
              </>
            )}
          </div>

          {/* Energy Components */}
          <div className="relative z-10 h-full">
            {/* Solar Panel */}
            <div className="absolute top-6 left-6 w-[180px]">
              <div
                className={`bg-gradient-to-br ${solarActive ? "from-amber-100 to-amber-200 dark:from-amber-900 dark:to-amber-800" : "from-slate-100 to-slate-200 dark:from-slate-800 dark:to-slate-700"} p-4 rounded-lg shadow-md`}
              >
                <div className="flex items-center justify-between mb-2">
                  <Sun className={`${solarActive ? "text-amber-500" : "text-slate-400"}`} size={28} />
                  <span className="text-sm font-medium">{solarOutput}%</span>
                </div>
                <h3 className="font-medium">Solarpanel</h3>
                <Progress value={solarOutput} className="h-1.5 mt-2" />
                <div className="mt-2 text-xs text-slate-500 dark:text-slate-400">
                  {solarActive ? "Aktiv" : "Inaktiv"}
                  {solarActive && weather === "cloudy" && " • Bewölkt"}
                </div>
              </div>
            </div>

            {/* Battery */}
            <div className="absolute top-6 right-6 w-[180px]">
              <div className="bg-gradient-to-br from-emerald-100 to-emerald-200 dark:from-emerald-900 dark:to-emerald-800 p-4 rounded-lg shadow-md">
                <div className="flex items-center justify-between mb-2">
                  <Battery
                    className={`${batteryCharging ? "text-emerald-500" : batteryLevel < 20 ? "text-red-500" : "text-emerald-500"}`}
                    size={28}
                  />
                  <span className="text-sm font-medium">{batteryLevel}%</span>
                </div>
                <h3 className="font-medium">Batterie</h3>
                <Progress value={batteryLevel} className="h-1.5 mt-2" />
                <div className="mt-2 text-xs text-slate-500 dark:text-slate-400">
                  {batteryCharging ? "Wird geladen" : batteryToHome > 0 ? "Entlädt" : "Standby"}
                </div>
              </div>
            </div>

            {/* Grid */}
            <div className="absolute bottom-6 left-6 w-[180px]">
              <div
                className={`bg-gradient-to-br ${gridActive ? "from-blue-100 to-blue-200 dark:from-blue-900 dark:to-blue-800" : "from-slate-100 to-slate-200 dark:from-slate-800 dark:to-slate-700"} p-4 rounded-lg shadow-md`}
              >
                <div className="flex items-center justify-between mb-2">
                  <Power className={`${gridActive ? "text-blue-500" : "text-slate-400"}`} size={28} />
                  <span className="text-sm font-medium">
                    {gridActive ? (gridToHome > 0 ? "Import" : solarToGrid > 0 ? "Export" : "Standby") : "Getrennt"}
                  </span>
                </div>
                <h3 className="font-medium">Stromnetz</h3>
                <div className="flex justify-between mt-2 text-xs">
                  <span>{gridToHome > 0 ? `${gridToHome}% Import` : ""}</span>
                  <span>{solarToGrid > 0 ? `${solarToGrid}% Export` : ""}</span>
                </div>
                <div className="mt-2 text-xs text-slate-500 dark:text-slate-400">
                  {gridActive ? "Verbunden" : "Getrennt"}
                </div>
              </div>
            </div>

            {/* Home */}
            <div className="absolute bottom-6 right-6 w-[180px]">
              <div className="bg-gradient-to-br from-purple-100 to-purple-200 dark:from-purple-900 dark:to-purple-800 p-4 rounded-lg shadow-md">
                <div className="flex items-center justify-between mb-2">
                  <Home className="text-purple-500" size={28} />
                  <span className="text-sm font-medium">{consumption}%</span>
                </div>
                <h3 className="font-medium">Haushalt</h3>
                <Progress value={consumption} className="h-1.5 mt-2" />
                <div className="mt-2 text-xs text-slate-500 dark:text-slate-400">Aktueller Verbrauch</div>
                <div className="mt-2">
                  <Slider
                    value={[consumption]}
                    onValueChange={(value) => setConsumption(value[0])}
                    min={10}
                    max={100}
                    step={5}
                    className="w-full"
                  />
                </div>
              </div>
            </div>

            {/* Energy Flow Lines */}
            <svg
              className="absolute inset-0 w-full h-full pointer-events-none"
              viewBox="0 0 800 500"
              preserveAspectRatio="none"
            >
              {/* Solar to Home */}
              <g className={getFlowIntensity(solarToHome)}>
                <path
                  d="M180,100 C300,150 500,350 620,400"
                  stroke="url(#solar-gradient)"
                  strokeWidth="4"
                  fill="none"
                  strokeLinecap="round"
                />
                {solarToHome > 0 && (
                  <g className={getAnimationSpeed(solarToHome)}>
                    <circle r="4" fill="#FFB800" className="animate-flow-along-path">
                      <animateMotion path="M180,100 C300,150 500,350 620,400" dur="3s" repeatCount="indefinite" />
                    </circle>
                    <circle r="4" fill="#FFB800" className="animate-flow-along-path">
                      <animateMotion
                        path="M180,100 C300,150 500,350 620,400"
                        dur="3s"
                        begin="1s"
                        repeatCount="indefinite"
                      />
                    </circle>
                    <circle r="4" fill="#FFB800" className="animate-flow-along-path">
                      <animateMotion
                        path="M180,100 C300,150 500,350 620,400"
                        dur="3s"
                        begin="2s"
                        repeatCount="indefinite"
                      />
                    </circle>
                  </g>
                )}
              </g>

              {/* Solar to Battery */}
              <g className={getFlowIntensity(solarToBattery)}>
                <path
                  d="M180,100 C300,50 500,50 620,100"
                  stroke="url(#solar-gradient)"
                  strokeWidth="4"
                  fill="none"
                  strokeLinecap="round"
                />
                {solarToBattery > 0 && (
                  <g className={getAnimationSpeed(solarToBattery)}>
                    <circle r="4" fill="#FFB800" className="animate-flow-along-path">
                      <animateMotion path="M180,100 C300,50 500,50 620,100" dur="3s" repeatCount="indefinite" />
                    </circle>
                    <circle r="4" fill="#FFB800" className="animate-flow-along-path">
                      <animateMotion
                        path="M180,100 C300,50 500,50 620,100"
                        dur="3s"
                        begin="1s"
                        repeatCount="indefinite"
                      />
                    </circle>
                    <circle r="4" fill="#FFB800" className="animate-flow-along-path">
                      <animateMotion
                        path="M180,100 C300,50 500,50 620,100"
                        dur="3s"
                        begin="2s"
                        repeatCount="indefinite"
                      />
                    </circle>
                  </g>
                )}
              </g>

              {/* Battery to Home */}
              <g className={getFlowIntensity(batteryToHome)}>
                <path
                  d="M620,100 C620,200 620,300 620,400"
                  stroke="url(#battery-gradient)"
                  strokeWidth="4"
                  fill="none"
                  strokeLinecap="round"
                />
                {batteryToHome > 0 && batteryLevel > 10 && (
                  <g className={getAnimationSpeed(batteryToHome)}>
                    <circle r="4" fill="#10B981" className="animate-flow-along-path">
                      <animateMotion path="M620,100 C620,200 620,300 620,400" dur="2s" repeatCount="indefinite" />
                    </circle>
                    <circle r="4" fill="#10B981" className="animate-flow-along-path">
                      <animateMotion
                        path="M620,100 C620,200 620,300 620,400"
                        dur="2s"
                        begin="0.7s"
                        repeatCount="indefinite"
                      />
                    </circle>
                    <circle r="4" fill="#10B981" className="animate-flow-along-path">
                      <animateMotion
                        path="M620,100 C620,200 620,300 620,400"
                        dur="2s"
                        begin="1.4s"
                        repeatCount="indefinite"
                      />
                    </circle>
                  </g>
                )}
              </g>

              {/* Grid to Home */}
              <g className={getFlowIntensity(gridToHome)}>
                <path
                  d="M180,400 C300,450 500,450 620,400"
                  stroke="url(#grid-gradient)"
                  strokeWidth="4"
                  fill="none"
                  strokeLinecap="round"
                />
                {gridToHome > 0 && (
                  <g className={getAnimationSpeed(gridToHome)}>
                    <circle r="4" fill="#3B82F6" className="animate-flow-along-path">
                      <animateMotion path="M180,400 C300,450 500,450 620,400" dur="3s" repeatCount="indefinite" />
                    </circle>
                    <circle r="4" fill="#3B82F6" className="animate-flow-along-path">
                      <animateMotion
                        path="M180,400 C300,450 500,450 620,400"
                        dur="3s"
                        begin="1s"
                        repeatCount="indefinite"
                      />
                    </circle>
                    <circle r="4" fill="#3B82F6" className="animate-flow-along-path">
                      <animateMotion
                        path="M180,400 C300,450 500,450 620,400"
                        dur="3s"
                        begin="2s"
                        repeatCount="indefinite"
                      />
                    </circle>
                  </g>
                )}
              </g>

              {/* Solar to Grid */}
              <g className={getFlowIntensity(solarToGrid)}>
                <path
                  d="M180,100 C180,200 180,300 180,400"
                  stroke="url(#solar-gradient)"
                  strokeWidth="4"
                  fill="none"
                  strokeLinecap="round"
                />
                {solarToGrid > 0 && (
                  <g className={getAnimationSpeed(solarToGrid)}>
                    <circle r="4" fill="#FFB800" className="animate-flow-along-path">
                      <animateMotion path="M180,100 C180,200 180,300 180,400" dur="2s" repeatCount="indefinite" />
                    </circle>
                    <circle r="4" fill="#FFB800" className="animate-flow-along-path">
                      <animateMotion
                        path="M180,100 C180,200 180,300 180,400"
                        dur="2s"
                        begin="0.7s"
                        repeatCount="indefinite"
                      />
                    </circle>
                    <circle r="4" fill="#FFB800" className="animate-flow-along-path">
                      <animateMotion
                        path="M180,100 C180,200 180,300 180,400"
                        dur="2s"
                        begin="1.4s"
                        repeatCount="indefinite"
                      />
                    </circle>
                  </g>
                )}
              </g>

              {/* Gradients */}
              <defs>
                <linearGradient id="solar-gradient" x1="0%" y1="0%" x2="100%" y2="0%">
                  <stop offset="0%" stopColor="#FFB800" />
                  <stop offset="100%" stopColor="#FCD34D" />
                </linearGradient>
                <linearGradient id="battery-gradient" x1="0%" y1="0%" x2="0%" y2="100%">
                  <stop offset="0%" stopColor="#10B981" />
                  <stop offset="100%" stopColor="#34D399" />
                </linearGradient>
                <linearGradient id="grid-gradient" x1="0%" y1="0%" x2="100%" y2="0%">
                  <stop offset="0%" stopColor="#3B82F6" />
                  <stop offset="100%" stopColor="#60A5FA" />
                </linearGradient>
              </defs>
            </svg>

            {/* Energy Flow Legend */}
            <div className="absolute left-1/2 top-1/2 transform -translate-x-1/2 -translate-y-1/2 bg-white/90 dark:bg-slate-800/90 p-4 rounded-lg shadow-lg">
              <h3 className="font-medium text-center mb-2">Energiefluss</h3>
              <div className="space-y-2">
                <div className="flex items-center gap-2">
                  <div className="w-3 h-3 rounded-full bg-amber-400"></div>
                  <span className="text-sm">Solar: {solarOutput}%</span>
                </div>
                <div className="flex items-center gap-2">
                  <div className="w-3 h-3 rounded-full bg-emerald-500"></div>
                  <span className="text-sm">Batterie: {batteryLevel}%</span>
                </div>
                <div className="flex items-center gap-2">
                  <div className="w-3 h-3 rounded-full bg-blue-500"></div>
                  <span className="text-sm">
                    Netz: {gridToHome > 0 ? `${gridToHome}% Import` : solarToGrid > 0 ? `${solarToGrid}% Export` : "0%"}
                  </span>
                </div>
                <div className="flex items-center gap-2">
                  <div className="w-3 h-3 rounded-full bg-purple-500"></div>
                  <span className="text-sm">Verbrauch: {consumption}%</span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </CardContent>
    </Card>
  )
}
