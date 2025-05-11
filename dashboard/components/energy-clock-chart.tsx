"use client"

import { useState, useEffect } from "react"
import { Battery, Bolt, Info, Lightbulb, Power, RefreshCw, Zap } from "lucide-react"
import { Card, Title, Text } from '@tremor/react'
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts'
import { format, parseISO } from 'date-fns'
import { de } from 'date-fns/locale'
import { TABLES } from '@/lib/constants'

import { Card as UICard, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs"
import {
  ChartArea,
  ChartAxisX,
  ChartAxisY,
  ChartContainer,
  ChartGrid,
  ChartLine,
  ChartTooltip,
  ChartTooltipContent,
} from "@/components/ui/chart"
import type { EnergyData } from "@/lib/data-service"
import { generate24HourData } from "@/lib/data-service"

interface EnergyClockChartProps {
  data: EnergyData
  isRefreshing?: boolean
}

export function EnergyClockChart({ data, isRefreshing = false }: EnergyClockChartProps) {
  // Alle Hooks am Anfang der Komponente
  const [mounted, setMounted] = useState(false);
  const [hoveredHour, setHoveredHour] = useState<number | null>(null);
  const [timelineData] = useState(() => generate24HourData());
  const [selectedTimelineChart, setSelectedTimelineChart] = useState<string>("all");

  useEffect(() => {
    setMounted(true);
  }, []);

  // Wenn die Komponente noch nicht client-seitig gemounted ist, zeigen wir einen Platzhalter
  if (!mounted) {
    return (
      <div className="relative m-auto aspect-square w-full max-w-[500px]">
        <div className="animate-pulse bg-gray-200 rounded-full w-full h-full" />
      </div>
    );
  }

  // Helper functions for power flow visualization
  const getArrowColor = (value: number) => {
    if (value === 0) return "stroke-gray-300"
    return "stroke-current text-primary"
  }

  const getArrowWidth = (value: number) => {
    if (value === 0) return 1
    return 1 + value * 3
  }

  const getArrowOpacity = (value: number) => {
    if (value === 0) return 0.3
    return 0.8
  }

  const currentHour = data.timestamp.getHours()
  const currentSource = data.hourlyRecommendations.find((rec) => rec.hour === currentHour)?.source || "unknown"

  // Determine which hour and source to display in the center
  const displayHour = hoveredHour !== null ? hoveredHour : currentHour
  const displaySource =
    hoveredHour !== null
      ? data.hourlyRecommendations.find((rec) => rec.hour === hoveredHour)?.source || "unknown"
      : currentSource

  const getBackgroundColorWithTransparency = (source: string) => {
    switch (source) {
      case "solar-to-battery":
        return "rgba(234, 179, 8, 0.1)" // yellow-500 with low opacity
      case "solar-direct":
        return "rgba(249, 115, 22, 0.1)" // orange-500 with low opacity
      case "battery":
        return "rgba(34, 197, 94, 0.1)" // green-500 with low opacity
      case "grid":
        return "rgba(59, 130, 246, 0.1)" // blue-500 with low opacity
      default:
        return "rgba(209, 213, 219, 0.1)" // gray-300 with low opacity
    }
  }

  // Format hours for x-axis labels
  const formatHour = (hour: number) => {
    return `${hour}:00`
  }

  // Get max value for a specific data key across all timeline data
  const getMaxValue = (key: string) => {
    return Math.max(...timelineData.map((item) => item[key as keyof typeof item] as number)) * 1.1
  }

  return (
    <UICard className="col-span-2 relative">
      {isRefreshing && (
        <div className="absolute right-4 top-4 animate-spin text-muted-foreground">
          <RefreshCw className="h-4 w-4" />
        </div>
      )}
      <CardHeader>
        <CardTitle>Energy Usage Clock</CardTitle>
        <CardDescription>
          Optimal times for using different energy sources on{" "}
          {data.timestamp.toLocaleDateString([], { month: "short", day: "numeric" })}
        </CardDescription>
      </CardHeader>
      <CardContent>
        <Tabs defaultValue="clock">
          <TabsList className="mb-4">
            <TabsTrigger value="clock">Clock View</TabsTrigger>
            <TabsTrigger value="powerflow">Power Flow</TabsTrigger>
            <TabsTrigger value="analytics">Analytics</TabsTrigger>
          </TabsList>
          <TabsContent
            value="clock"
            className="pt-2 rounded-md transition-colors duration-300"
            style={{ backgroundColor: getBackgroundColorWithTransparency(currentSource) }}
          >
            <div className="relative mx-auto aspect-square max-w-[500px] p-4">
              {/* Main SVG with expanded viewBox to ensure all elements are visible */}
              <svg className="h-full w-full" viewBox="-5 -5 110 110">
                {/* Hour markers - only numbers, no outer ring */}
                {Array.from({ length: 24 }).map((_, i) => {
                  const angle = i * 15 * (Math.PI / 180)
                  return (
                    <g key={i}>
                      {/* Hour number */}
                      <text
                        x={50 + 48 * Math.sin(angle)}
                        y={50 - 48 * Math.cos(angle)}
                        textAnchor="middle"
                        dominantBaseline="middle"
                        fontSize="4"
                        fontWeight="medium"
                      >
                        {i}
                      </text>
                    </g>
                  )
                })}

                {/* Colored segments for different energy sources */}
                {data.hourlyRecommendations.map((hourData, i) => {
                  const startAngle = hourData.hour * 15 - 90
                  const endAngle = (hourData.hour + 1) * 15 - 90

                  const startRad = (startAngle * Math.PI) / 180
                  const endRad = (endAngle * Math.PI) / 180

                  const innerRadius = 20
                  const outerRadius = 45

                  const x1 = 50 + innerRadius * Math.cos(startRad)
                  const y1 = 50 + innerRadius * Math.sin(startRad)
                  const x2 = 50 + outerRadius * Math.cos(startRad)
                  const y2 = 50 + outerRadius * Math.sin(startRad)
                  const x3 = 50 + outerRadius * Math.cos(endRad)
                  const y3 = 50 + outerRadius * Math.sin(endRad)
                  const x4 = 50 + innerRadius * Math.cos(endRad)
                  const y4 = 50 + innerRadius * Math.sin(endRad)

                  // Arc flag is always 0 for arcs less than 180 degrees
                  const arcFlag = 0
                  // Sweep flag is 1 for clockwise
                  const sweepFlag = 1

                  let color
                  switch (hourData.source) {
                    case "solar-to-battery":
                      color = "rgba(234, 179, 8, 0.9)" // yellow-500 with higher opacity
                      break
                    case "solar-direct":
                      color = "rgba(249, 115, 22, 0.9)" // orange-500 with higher opacity
                      break
                    case "battery":
                      color = "rgba(34, 197, 94, 0.9)" // green-500 with higher opacity
                      break
                    case "grid":
                      color = "rgba(59, 130, 246, 0.9)" // blue-500 with higher opacity
                      break
                    default:
                      color = "rgba(209, 213, 219, 0.9)" // gray-300 with higher opacity
                  }

                  // For the current hour or hovered hour, add a highlight
                  const isCurrentHour = hourData.hour === currentHour
                  const isHovered = hourData.hour === hoveredHour
                  const strokeWidth = isCurrentHour ? 2 : isHovered ? 1.5 : 0
                  const strokeColor = isCurrentHour
                    ? "rgba(239, 68, 68, 1)"
                    : isHovered
                      ? "rgba(255, 255, 255, 0.8)"
                      : "transparent"

                  return (
                    <path
                      key={i}
                      d={`
                        M ${x1} ${y1}
                        L ${x2} ${y2}
                        A ${outerRadius} ${outerRadius} 0 ${arcFlag} ${sweepFlag} ${x3} ${y3}
                        L ${x4} ${y4}
                        A ${innerRadius} ${innerRadius} 0 ${arcFlag} ${1 - sweepFlag} ${x1} ${y1}
                      `}
                      fill={color}
                      stroke={strokeColor}
                      strokeWidth={strokeWidth}
                      onMouseEnter={() => setHoveredHour(hourData.hour)}
                      onMouseLeave={() => setHoveredHour(null)}
                      style={{ cursor: "pointer" }}
                    />
                  )
                })}

                {/* Current time indicator - more like a traditional clock hand */}
                {(() => {
                  const minuteAngle = currentHour * 15 + (data.timestamp.getMinutes() * 15) / 60 - 90
                  const minuteRad = (minuteAngle * Math.PI) / 180

                  // Calculate points for a tapered clock hand
                  const handLength = 45
                  const x1 = 50 // center x
                  const y1 = 50 // center y
                  const x2 = 50 + handLength * Math.cos(minuteRad)
                  const y2 = 50 + handLength * Math.sin(minuteRad)

                  // Calculate points for the sides of the tapered hand
                  const width = 1.5 // width of the hand at the base
                  const perpRad = minuteRad + Math.PI / 2 // perpendicular angle
                  const x1Left = x1 + width * Math.cos(perpRad)
                  const y1Left = y1 + width * Math.sin(perpRad)
                  const x1Right = x1 - width * Math.cos(perpRad)
                  const y1Right = y1 - width * Math.sin(perpRad)

                  return (
                    <>
                      {/* Tapered hand */}
                      <path
                        d={`M ${x1Left} ${y1Left} L ${x2} ${y2} L ${x1Right} ${y1Right} Z`}
                        fill="rgba(0, 0, 0, 0.9)"
                        stroke="rgba(0, 0, 0, 1)"
                        strokeWidth="0.5"
                      />

                      {/* Center pin */}
                      <circle cx="50" cy="50" r="1.5" fill="rgba(0, 0, 0, 1)" stroke="white" strokeWidth="0.5" />
                    </>
                  )
                })()}

                {/* Center of clock with current or hovered recommendation */}
                {(() => {
                  let centerColor
                  const textColor = "white"
                  let recommendationText = ""

                  switch (displaySource) {
                    case "solar-to-battery":
                      centerColor = "rgba(234, 179, 8, 1)" // yellow-500
                      recommendationText = "Charge Battery"
                      break
                    case "solar-direct":
                      centerColor = "rgba(249, 115, 22, 1)" // orange-500
                      recommendationText = "Use Solar"
                      break
                    case "battery":
                      centerColor = "rgba(34, 197, 94, 1)" // green-500
                      recommendationText = "Use Battery"
                      break
                    case "grid":
                      centerColor = "rgba(59, 130, 246, 1)" // blue-500
                      recommendationText = "Use Grid"
                      break
                    default:
                      centerColor = "rgba(209, 213, 219, 1)" // gray-300
                      recommendationText = "Unknown"
                  }

                  return (
                    <>
                      {/* Background circle with black border */}
                      <circle cx="50" cy="50" r="20" fill={centerColor} stroke="black" strokeWidth="0.5" />

                      {/* Time display */}
                      <text x="50" y="45" textAnchor="middle" fontSize="5" fontWeight="bold" fill={textColor}>
                        {displayHour}:00
                      </text>

                      {/* Recommendation text */}
                      <text x="50" y="52" textAnchor="middle" fontSize="3.5" fontWeight="medium" fill={textColor}>
                        {recommendationText}
                      </text>

                      {/* Status text */}
                      <text x="50" y="58" textAnchor="middle" fontSize="2.5" fill={textColor} opacity="0.8">
                        {hoveredHour !== null ? "Hover Information" : "Current Recommendation"}
                      </text>
                    </>
                  )
                })()}
              </svg>
            </div>

            {/* Legend */}
            <div className="mt-8 grid grid-cols-2 gap-4 sm:grid-cols-4 items-center">
              <div className="flex items-center gap-2">
                <div className="h-4 w-4 rounded-full bg-yellow-500"></div>
                <span className="text-sm">Charge Battery</span>
              </div>
              <div className="flex items-center gap-2">
                <div className="h-4 w-4 rounded-full bg-orange-500"></div>
                <span className="text-sm">Use Solar Direct</span>
              </div>
              <div className="flex items-center gap-2">
                <div className="h-4 w-4 rounded-full bg-green-500"></div>
                <span className="text-sm">Use Battery</span>
              </div>
              <div className="flex items-center gap-2">
                <div className="h-4 w-4 rounded-full bg-blue-500"></div>
                <span className="text-sm">Use Grid</span>
              </div>
            </div>
          </TabsContent>


          <TabsContent value="powerflow">
            <div className="space-y-4">
              <div className="relative h-64 w-full">
                <svg className="h-full w-full" viewBox="0 0 400 250">
                  {/* Background */}
                  <rect x="0" y="0" width="400" height="250" fill="transparent" />

                  {/* Solar Panel */}
                  <g transform="translate(180, 30)">
                    <rect
                      x="-30"
                      y="-20"
                      width="60"
                      height="40"
                      rx="5"
                      fill="rgba(234, 179, 8, 0.2)"
                      stroke="rgba(234, 179, 8, 0.8)"
                      strokeWidth="1.5"
                    />
                    <text x="0" y="5" textAnchor="middle" fontSize="12" fontWeight="bold">
                      Solar
                    </text>
                    <path
                      d="M-20 -10 L-10 -10 L-10 0 L0 0 L0 -10 L10 -10 L10 0 L20 0 L20 -10"
                      stroke="rgba(234, 179, 8, 0.8)"
                      strokeWidth="1.5"
                      fill="none"
                    />
                  </g>

                  {/* Battery */}
                  <g transform="translate(80, 130)">
                    <rect
                      x="-30"
                      y="-20"
                      width="60"
                      height="40"
                      rx="5"
                      fill="rgba(34, 197, 94, 0.2)"
                      stroke="rgba(34, 197, 94, 0.8)"
                      strokeWidth="1.5"
                    />
                    <text x="0" y="5" textAnchor="middle" fontSize="12" fontWeight="bold">
                      Battery
                    </text>
                    <rect
                      x="-15"
                      y="-8"
                      width="30"
                      height="16"
                      rx="2"
                      fill="none"
                      stroke="rgba(34, 197, 94, 0.8)"
                      strokeWidth="1.5"
                    />
                    <rect x="15" y="-4" width="4" height="8" fill="rgba(34, 197, 94, 0.8)" />
                  </g>

                  {/* Home */}
                  <g transform="translate(280, 130)">
                    <rect
                      x="-30"
                      y="-20"
                      width="60"
                      height="40"
                      rx="5"
                      fill="rgba(249, 115, 22, 0.2)"
                      stroke="rgba(249, 115, 22, 0.8)"
                      strokeWidth="1.5"
                    />
                    <text x="0" y="5" textAnchor="middle" fontSize="12" fontWeight="bold">
                      Home
                    </text>
                    <path
                      d="M-15 10 L-15 -5 L0 -15 L15 -5 L15 10"
                      fill="none"
                      stroke="rgba(249, 115, 22, 0.8)"
                      strokeWidth="1.5"
                    />
                    <rect
                      x="-5"
                      y="0"
                      width="10"
                      height="10"
                      fill="none"
                      stroke="rgba(249, 115, 22, 0.8)"
                      strokeWidth="1.5"
                    />
                  </g>

                  {/* Grid */}
                  <g transform="translate(180, 220)">
                    <rect
                      x="-30"
                      y="-20"
                      width="60"
                      height="40"
                      rx="5"
                      fill="rgba(59, 130, 246, 0.2)"
                      stroke="rgba(59, 130, 246, 0.8)"
                      strokeWidth="1.5"
                    />
                    <text x="0" y="5" textAnchor="middle" fontSize="12" fontWeight="bold">
                      Grid
                    </text>
                    <path
                      d="M-15 -8 L15 -8 M-15 0 L15 0 M-15 8 L15 8"
                      stroke="rgba(59, 130, 246, 0.8)"
                      strokeWidth="1.5"
                      fill="none"
                    />
                  </g>

                  {/* Power Flow Arrows */}

                  {/* Solar to Battery */}
                  <g opacity={getArrowOpacity(data.powerFlow.solarToBattery)}>
                    <path
                      d="M150 50 C120 50, 100 80, 100 110"
                      fill="none"
                      className={getArrowColor(data.powerFlow.solarToBattery)}
                      strokeWidth={getArrowWidth(data.powerFlow.solarToBattery)}
                      strokeDasharray={data.powerFlow.solarToBattery > 0 ? "0" : "4 2"}
                    />
                    {data.powerFlow.solarToBattery > 0 && (
                      <polygon points="100,110 95,100 105,100" className="fill-current text-primary" />
                    )}
                    {data.powerFlow.solarToBattery > 0 && (
                      <text
                        x="110"
                        y="70"
                        textAnchor="middle"
                        fontSize="10"
                        fontWeight="bold"
                        className="fill-current text-primary"
                      >
                        {(data.powerFlow.solarToBattery * 1000).toFixed(0)} W
                      </text>
                    )}
                  </g>

                  {/* Solar to Home */}
                  <g opacity={getArrowOpacity(data.powerFlow.solarToHome)}>
                    <path
                      d="M210 50 C240 50, 260 80, 260 110"
                      fill="none"
                      className={getArrowColor(data.powerFlow.solarToHome)}
                      strokeWidth={getArrowWidth(data.powerFlow.solarToHome)}
                      strokeDasharray={data.powerFlow.solarToHome > 0 ? "0" : "4 2"}
                    />
                    {data.powerFlow.solarToHome > 0 && (
                      <polygon points="260,110 255,100 265,100" className="fill-current text-primary" />
                    )}
                    {data.powerFlow.solarToHome > 0 && (
                      <text
                        x="250"
                        y="70"
                        textAnchor="middle"
                        fontSize="10"
                        fontWeight="bold"
                        className="fill-current text-primary"
                      >
                        {(data.powerFlow.solarToHome * 1000).toFixed(0)} W
                      </text>
                    )}
                  </g>

                  {/* Battery to Home */}
                  <g opacity={getArrowOpacity(data.powerFlow.batteryToHome)}>
                    <path
                      d="M110 130 L250 130"
                      fill="none"
                      className={getArrowColor(data.powerFlow.batteryToHome)}
                      strokeWidth={getArrowWidth(data.powerFlow.batteryToHome)}
                      strokeDasharray={data.powerFlow.batteryToHome > 0 ? "0" : "4 2"}
                    />
                    {data.powerFlow.batteryToHome > 0 && (
                      <polygon points="250,130 240,125 240,135" className="fill-current text-primary" />
                    )}
                    {data.powerFlow.batteryToHome > 0 && (
                      <text
                        x="180"
                        y="125"
                        textAnchor="middle"
                        fontSize="10"
                        fontWeight="bold"
                        className="fill-current text-primary"
                      >
                        {(data.powerFlow.batteryToHome * 1000).toFixed(0)} W
                      </text>
                    )}
                  </g>

                  {/* Grid to Home */}
                  <g opacity={getArrowOpacity(data.powerFlow.gridToHome)}>
                    <path
                      d="M180 200 C180 180, 230 180, 250 150"
                      fill="none"
                      className={getArrowColor(data.powerFlow.gridToHome)}
                      strokeWidth={getArrowWidth(data.powerFlow.gridToHome)}
                      strokeDasharray={data.powerFlow.gridToHome > 0 ? "0" : "4 2"}
                    />
                    {data.powerFlow.gridToHome > 0 && (
                      <polygon points="250,150 240,155 245,165" className="fill-current text-primary" />
                    )}
                    {data.powerFlow.gridToHome > 0 && (
                      <text
                        x="230"
                        y="180"
                        textAnchor="middle"
                        fontSize="10"
                        fontWeight="bold"
                        className="fill-current text-primary"
                      >
                        {(data.powerFlow.gridToHome * 1000).toFixed(0)} W
                      </text>
                    )}
                  </g>

                  {/* Battery to Grid (for selling back) */}
                  <g opacity={getArrowOpacity(data.powerFlow.batteryToGrid)}>
                    <path
                      d="M100 150 C100 180, 130 200, 150 200"
                      fill="none"
                      className={getArrowColor(data.powerFlow.batteryToGrid)}
                      strokeWidth={getArrowWidth(data.powerFlow.batteryToGrid)}
                      strokeDasharray={data.powerFlow.batteryToGrid > 0 ? "0" : "4 2"}
                    />
                    {data.powerFlow.batteryToGrid > 0 && (
                      <polygon points="150,200 140,195 140,205" className="fill-current text-primary" />
                    )}
                    {data.powerFlow.batteryToGrid > 0 && (
                      <text
                        x="110"
                        y="180"
                        textAnchor="middle"
                        fontSize="10"
                        fontWeight="bold"
                        className="fill-current text-primary"
                      >
                        {(data.powerFlow.batteryToGrid * 1000).toFixed(0)} W
                      </text>
                    )}
                  </g>
                </svg>
              </div>

              <div className="mt-4 rounded-lg bg-muted p-3">
                <div className="flex items-center justify-between">
                  <div className="flex items-center gap-2">
                    <Power className="h-4 w-4 text-primary" />
                    <span className="text-sm font-medium">Total Power Flow</span>
                  </div>
                  <span className="font-medium">
                    {(
                      (data.powerFlow.solarToHome +
                        data.powerFlow.solarToBattery +
                        data.powerFlow.batteryToHome +
                        data.powerFlow.gridToHome) *
                      1000
                    ).toFixed(0)}{" "}
                    W
                  </span>
                </div>
              </div>
            </div>
          </TabsContent>

          <TabsContent value="analytics">
            <div className="flex flex-col space-y-2">
              {TABLES.map(table => {
                const chartData = data[table.id as keyof Pick<EnergyData, 'solar_output' | 'battery_storage_status' | 'grid_usage' | 'output_algorithm'>] || [];
                
                // Sortiere die Daten nach Timestamp
                const sortedData = [...chartData].sort((a, b) => {
                  try {
                    const dateA = new Date(a.timestamp);
                    const dateB = new Date(b.timestamp);
                    if (isNaN(dateA.getTime()) || isNaN(dateB.getTime())) return 0;
                    return dateA.getTime() - dateB.getTime();
                  } catch (e) {
                    console.error('Fehler beim Sortieren der Zeitstempel:', e);
                    return 0;
                  }
                });

                // Bestimme den Zeitraum für die Anzeige im Titel
                let timeRangeText = '';
                if (sortedData.length > 0) {
                  try {
                    const firstDate = new Date(sortedData[0].timestamp);
                    const lastDate = new Date(sortedData[sortedData.length - 1].timestamp);
                    if (!isNaN(firstDate.getTime()) && !isNaN(lastDate.getTime())) {
                      if (firstDate.toDateString() === lastDate.toDateString()) {
                        timeRangeText = format(lastDate, 'dd.MM.yyyy', { locale: de });
                      } else {
                        timeRangeText = `${format(firstDate, 'dd.MM.', { locale: de })} - ${format(lastDate, 'dd.MM.yyyy', { locale: de })}`;
                      }
                    }
                  } catch (e) {
                    console.error('Fehler bei der Zeitraum-Formatierung:', e);
                  }
                }

                return (
                  <Card key={table.id} className="p-3">
                    <Title className="text-sm mb-2">
                      {table.name}
                      <span className="text-xs text-muted-foreground ml-2">
                        {timeRangeText}
                      </span>
                    </Title>
                    <div className="h-[200px]">
                      <ResponsiveContainer width="100%" height="100%">
                        <LineChart 
                          data={sortedData}
                          margin={{ top: 5, right: 10, left: 5, bottom: 5 }}
                        >
                          <CartesianGrid strokeDasharray="3 3" />
                          <XAxis 
                            dataKey="timestamp"
                            angle={-45}
                            textAnchor="end"
                            height={50}
                            tick={{ fontSize: 10 }}
                            tickFormatter={(value) => {
                              try {
                                if (!value) return '';
                                const date = parseISO(value);
                                if (isNaN(date.getTime())) return '';
                                return format(date, 'dd.MM. HH:mm', { locale: de });
                              } catch (e) {
                                console.error('Fehler bei der Zeitstempel-Formatierung:', value);
                                return '';
                              }
                            }}
                            interval="preserveStartEnd"
                            minTickGap={50}
                            domain={['dataMin', 'dataMax']}
                          />
                          <YAxis 
                            tickFormatter={(value) => `${value.toFixed(1)} kW`}
                            tick={{ fontSize: 10 }}
                            width={50}
                            dx={-5}
                          />
                          <Tooltip 
                            formatter={(value: number) => [`${value.toFixed(2)} kW`, table.name]}
                            labelFormatter={(label) => {
                              try {
                                if (!label) return '';
                                const date = parseISO(label as string);
                                if (isNaN(date.getTime())) return '';
                                return format(date, 'dd.MM.yyyy HH:mm', { locale: de });
                              } catch (e) {
                                console.error('Fehler bei der Tooltip-Formatierung:', label);
                                return '';
                              }
                            }}
                          />
                          <Line 
                            type="monotone" 
                            dataKey="value" 
                            stroke={table.color} 
                            strokeWidth={2}
                            dot={false}
                            name={table.name}
                          />
                        </LineChart>
                      </ResponsiveContainer>
                    </div>
                  </Card>
                );
              })}
            </div>
          </TabsContent>
        </Tabs>
      </CardContent>
    </UICard>
  )
}

function Sun({ className }: { className?: string }) {
  return (
    <svg
      xmlns="http://www.w3.org/2000/svg"
      viewBox="0 0 24 24"
      fill="none"
      stroke="currentColor"
      strokeWidth="2"
      strokeLinecap="round"
      strokeLinejoin="round"
      className={className}
    >
      <circle cx="12" cy="12" r="4" />
      <path d="M12 2v2" />
      <path d="M12 20v2" />
      <path d="m4.93 4.93 1.41 1.41" />
      <path d="m17.66 17.66 1.41 1.41" />
      <path d="M2 12h2" />
      <path d="M20 12h2" />
      <path d="m6.34 17.66-1.41 1.41" />
      <path d="m19.07 4.93-1.41 1.41" />
    </svg>
  )
}
