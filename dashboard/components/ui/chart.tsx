"use client"

import * as React from "react"
import { cn } from "@/lib/utils"

interface ChartContainerProps extends React.HTMLAttributes<HTMLDivElement> {
  data: any[]
}

const ChartContainer = React.forwardRef<HTMLDivElement, ChartContainerProps>(
  ({ className, data, children, ...props }, ref) => {
    return (
      <div className={cn("relative", className)} ref={ref} {...props}>
        <Chart data={data}>{children}</Chart>
      </div>
    )
  },
)
ChartContainer.displayName = "ChartContainer"

interface ChartGridProps extends React.SVGAttributes<SVGSVGElement> {
  horizontal?: boolean
  vertical?: boolean
}

const ChartGrid = React.forwardRef<SVGSVGElement, ChartGridProps>(
  ({ className, horizontal, vertical, ...props }, ref) => {
    return (
      <svg ref={ref} className={cn("absolute inset-0 h-full w-full stroke-muted", className)} {...props}>
        {horizontal && <line x1="0" y1="25%" x2="100%" y2="25%" strokeDasharray="4 4" />}
        {horizontal && <line x1="0" y1="50%" x2="100%" y2="50%" strokeDasharray="4 4" />}
        {horizontal && <line x1="0" y1="75%" x2="100%" y2="75%" strokeDasharray="4 4" />}
        {vertical && <line x1="25%" y1="0" x2="25%" y2="100%" strokeDasharray="4 4" />}
        {vertical && <line x1="50%" y1="0" x2="50%" y2="100%" strokeDasharray="4 4" />}
        {vertical && <line x1="75%" y1="0" x2="75%" y2="100%" strokeDasharray="4 4" />}
      </svg>
    )
  },
)
ChartGrid.displayName = "ChartGrid"

interface ChartLineProps extends React.SVGAttributes<SVGSVGElement> {
  curve?: "linear" | "monotone" | "step" | "catmullRom"
  valueKey: string
  pathClassName?: string
  pointClassName?: string
}

const ChartLine = React.forwardRef<SVGSVGElement, ChartLineProps>(
  ({ className, curve = "linear", valueKey, pathClassName, pointClassName, ...props }, ref) => {
    const chartContext = React.useContext(ChartContext)
    if (!chartContext) return null

    const { data } = chartContext

    const points = data.map((item) => item[valueKey]).filter((value) => value !== null) as number[]
    const maxValue = Math.max(...points)
    const stepX = 100 / (points.length - 1)

    const path = points.reduce((acc, point, index) => {
      const x = stepX * index
      const y = 100 - (point / maxValue) * 100

      if (index === 0) {
        return `M${x},${y}`
      }

      if (curve === "linear") {
        return `${acc} L${x},${y}`
      }

      if (curve === "monotone") {
        const prevX = stepX * (index - 1)
        const prevY = 100 - (points[index - 1] / maxValue) * 100
        const deltaX = x - prevX
        const deltaY = y - prevY
        const controlPointDistance = Math.min(deltaX / 2, Math.abs(deltaY / 2))

        const controlPoint1X = prevX + controlPointDistance
        const controlPoint1Y = prevY

        const controlPoint2X = x - controlPointDistance
        const controlPoint2Y = y

        return `${acc} C${controlPoint1X},${controlPoint1Y} ${controlPoint2X},${controlPoint2Y} ${x},${y}`
      }

      return `${acc} L${x},${y}`
    }, "")

    return (
      <svg ref={ref} className={cn("absolute inset-0 h-full w-full fill-none stroke-current", className)} {...props}>
        <path className={cn("stroke-[3px]", pathClassName)} d={path} />
        {points.map((point, index) => {
          const x = stepX * index
          const y = 100 - (point / maxValue) * 100
          return (
            <circle
              key={index}
              cx={x}
              cy={y}
              r="3"
              className={cn("stroke-background fill-current stroke-[1.5px]", pointClassName)}
            />
          )
        })}
      </svg>
    )
  },
)
ChartLine.displayName = "ChartLine"

interface ChartAreaProps extends React.SVGAttributes<SVGSVGElement> {
  curve?: "linear" | "monotone" | "step" | "catmullRom"
  valueKey: string
}

const ChartArea = React.forwardRef<SVGSVGElement, ChartAreaProps>(
  ({ className, curve = "linear", valueKey, ...props }, ref) => {
    const chartContext = React.useContext(ChartContext)
    if (!chartContext) return null

    const { data } = chartContext

    const points = data.map((item) => item[valueKey]).filter((value) => value !== null) as number[]
    const maxValue = Math.max(...points)
    const stepX = 100 / (points.length - 1)

    const path = points.reduce((acc, point, index) => {
      const x = stepX * index
      const y = 100 - (point / maxValue) * 100

      if (index === 0) {
        return `M${x},${y}`
      }

      if (curve === "linear") {
        return `${acc} L${x},${y}`
      }

      if (curve === "monotone") {
        const prevX = stepX * (index - 1)
        const prevY = 100 - (points[index - 1] / maxValue) * 100
        const deltaX = x - prevX
        const deltaY = y - prevY
        const controlPointDistance = Math.min(deltaX / 2, Math.abs(deltaY / 2))

        const controlPoint1X = prevX + controlPointDistance
        const controlPoint1Y = prevY

        const controlPoint2X = x - controlPointDistance
        const controlPoint2Y = y

        return `${acc} C${controlPoint1X},${controlPoint1Y} ${controlPoint2X},${controlPoint2Y} ${x},${y}`
      }

      return `${acc} L${x},${y}`
    }, "")

    return (
      <svg ref={ref} className={cn("absolute inset-0 h-full w-full fill-none stroke-current", className)} {...props}>
        <path className="fill-current opacity-20" d={`${path} L100,100 L0,100 Z`} />
      </svg>
    )
  },
)
ChartArea.displayName = "ChartArea"

interface ChartAxisXProps extends React.SVGAttributes<SVGSVGElement> {
  tickCount?: number
  tickFormat?: (value: number) => string
}

const ChartAxisX = React.forwardRef<SVGSVGElement, ChartAxisXProps>(
  ({ className, tickCount = 6, tickFormat = (value) => value.toString(), ...props }, ref) => {
    return (
      <svg
        ref={ref}
        className={cn("absolute bottom-0 left-0 h-5 w-full text-xs text-muted-foreground", className)}
        {...props}
      >
        {Array.from({ length: tickCount }).map((_, index) => {
          const value = index * (24 / (tickCount - 1))
          const x = (index / (tickCount - 1)) * 100
          return (
            <g key={index} transform={`translate(${x}%, 0)`}>
              <line x1="0" y1="0" x2="0" y2="-5" className="stroke-muted" />
              <text x="0" y="15" textAnchor="middle">
                {tickFormat(value)}
              </text>
            </g>
          )
        })}
      </svg>
    )
  },
)
ChartAxisX.displayName = "ChartAxisX"

interface ChartAxisYProps extends React.SVGAttributes<SVGSVGElement> {
  tickCount?: number
  tickFormat?: (value: number) => string
}

const ChartAxisY = React.forwardRef<SVGSVGElement, ChartAxisYProps>(
  ({ className, tickCount = 4, tickFormat = (value) => value.toString(), ...props }, ref) => {
    return (
      <svg
        ref={ref}
        className={cn("absolute top-0 left-0 w-8 h-full text-xs text-muted-foreground", className)}
        {...props}
      >
        {Array.from({ length: tickCount }).map((_, index) => {
          const value = index * (10 / (tickCount - 1))
          const y = 100 - (index / (tickCount - 1)) * 100
          return (
            <g key={index} transform={`translate(0, ${y}%)`}>
              <line x1="0" y1="0" x2="5" y2="0" className="stroke-muted" />
              <text x="10" y="0" textAnchor="start" dominantBaseline="middle">
                {tickFormat(value)}
              </text>
            </g>
          )
        })}
      </svg>
    )
  },
)
ChartAxisY.displayName = "ChartAxisY"

interface ChartTooltipProps {
  children: React.ReactNode
}

const ChartTooltip = ({ children }: ChartTooltipProps) => {
  return <>{children}</>
}
ChartTooltip.displayName = "ChartTooltip"

interface ChartTooltipContentProps extends React.HTMLAttributes<HTMLDivElement> {
  children: React.ReactNode | ((props: { point: any }) => React.ReactNode)
}

const ChartTooltipContent = React.forwardRef<HTMLDivElement, ChartTooltipContentProps>(
  ({ className, children, ...props }, ref) => {
    // Mock point data for rendering
    const point = { hour: 12, value: 2.5 }

    return (
      <div
        ref={ref}
        className={cn("rounded-md border bg-popover p-4 text-sm text-popover-foreground shadow-sm", className)}
        {...props}
      >
        {typeof children === "function" ? children({ point }) : children}
      </div>
    )
  },
)
ChartTooltipContent.displayName = "ChartTooltipContent"

interface ChartContextType {
  data: any[]
}

const ChartContext = React.createContext<ChartContextType | null>(null)

interface ChartProps {
  children: React.ReactNode
  data: any[]
}

const Chart = ({ children, data }: ChartProps) => {
  return <ChartContext.Provider value={{ data }}>{children}</ChartContext.Provider>
}
Chart.displayName = "Chart"

export {
  Chart,
  ChartArea,
  ChartAxisX,
  ChartAxisY,
  ChartGrid,
  ChartLine,
  ChartContainer,
  ChartTooltip,
  ChartTooltipContent,
}
