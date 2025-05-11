import { CheckCircle2, Info, LightbulbIcon } from "lucide-react"

import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import type { EnergyData } from "@/lib/data-service"

interface RecommendationsProps {
  data: EnergyData
  isRefreshing?: boolean
}

export function Recommendations({ data, isRefreshing = false }: RecommendationsProps) {
  const currentHour = data.timestamp.getHours()
  const currentSource = data.hourlyRecommendations.find((rec) => rec.hour === currentHour)?.source || "unknown"

  // Generate recommendations based on current energy source
  const getRecommendations = () => {
    switch (currentSource) {
      case "solar-to-battery":
        return [
          "Run high-power appliances now to use direct solar power",
          "Charge electric devices while solar production is high",
          "Consider running washing machine or dishwasher now",
          "Excess energy is being stored in battery for later use",
        ]
      case "solar-direct":
        return [
          "Ideal time to use electricity-intensive appliances",
          "Solar production is being used directly in your home",
          "Minimize battery usage to preserve charge for evening",
          "Good time for home office equipment and air conditioning",
        ]
      case "battery":
        return [
          "Using stored battery power - good for essential devices",
          "Avoid running multiple high-power appliances simultaneously",
          "Battery is optimal for evening lighting and entertainment",
          "Grid electricity prices are typically higher now",
        ]
      case "grid":
        return [
          "Try to minimize energy usage during this period",
          "Delay high-consumption tasks until solar production returns",
          "Check if any unnecessary devices can be turned off",
          "Consider using lower power settings on essential appliances",
        ]
      default:
        return [
          "Monitor your energy usage patterns",
          "Balance consumption with available renewable sources",
          "Optimize device usage based on energy availability",
          "Check system status if recommendations seem incorrect",
        ]
    }
  }

  const recommendations = getRecommendations()

  // Get the appropriate icon and color based on the current source
  const getSourceStyles = () => {
    switch (currentSource) {
      case "solar-to-battery":
        return {
          icon: <LightbulbIcon className="h-5 w-5" />,
          bgColor: "bg-yellow-100 dark:bg-yellow-900",
          textColor: "text-yellow-600 dark:text-yellow-400",
        }
      case "solar-direct":
        return {
          icon: <LightbulbIcon className="h-5 w-5" />,
          bgColor: "bg-orange-100 dark:bg-orange-900",
          textColor: "text-orange-600 dark:text-orange-400",
        }
      case "battery":
        return {
          icon: <LightbulbIcon className="h-5 w-5" />,
          bgColor: "bg-green-100 dark:bg-green-900",
          textColor: "text-green-600 dark:text-green-400",
        }
      case "grid":
        return {
          icon: <LightbulbIcon className="h-5 w-5" />,
          bgColor: "bg-blue-100 dark:bg-blue-900",
          textColor: "text-blue-600 dark:text-blue-400",
        }
      default:
        return {
          icon: <Info className="h-5 w-5" />,
          bgColor: "bg-gray-100 dark:bg-gray-800",
          textColor: "text-gray-600 dark:text-gray-400",
        }
    }
  }

  // Get background color with transparency based on the current source
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

  const { icon, bgColor, textColor } = getSourceStyles()

  return (
    <Card style={{ backgroundColor: getBackgroundColorWithTransparency(currentSource) }}>
      <CardHeader className="pb-2">
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-2">
            <div className={`rounded-full ${bgColor} p-1.5 ${textColor}`}>{icon}</div>
            <div>
              <CardTitle className="flex items-center gap-2">
                Current Recommendations
                <span className="text-sm font-normal text-muted-foreground ml-2">
                  {data.timestamp.toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" })}
                </span>
              </CardTitle>
            </div>
          </div>
        </div>
        <CardDescription>
          Optimize your energy usage during the current {getSourceLabel(currentSource)} phase
        </CardDescription>
      </CardHeader>
      <CardContent>
        <ul className="space-y-2">
          {recommendations.map((recommendation, index) => (
            <li key={index} className="flex items-start gap-2">
              <CheckCircle2 className="mt-0.5 h-4 w-4 text-primary shrink-0" />
              <span className="text-sm">{recommendation}</span>
            </li>
          ))}
        </ul>
      </CardContent>
    </Card>
  )
}

// Helper function to get a user-friendly label for the energy source
function getSourceLabel(source: string): string {
  switch (source) {
    case "solar-to-battery":
      return "battery charging"
    case "solar-direct":
      return "direct solar"
    case "battery":
      return "battery usage"
    case "grid":
      return "grid usage"
    default:
      return "energy"
  }
}
