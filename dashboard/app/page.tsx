"use client"

import { useEffect, useState } from "react"

import { DashboardHeader } from "@/components/dashboard-header"
import { EnergyClockChart } from "@/components/energy-clock-chart"
import { EnergyStats } from "@/components/energy-stats"
import { HistoricGraphSlider } from "@/components/historic-graph-slider"
import { Recommendations } from "@/components/recommendations"
import {
  type EnergyData,
  fetchCurrentData,
  fetchHistoricData,
  getInitialMockupData,
  getHistoricMockupData,
} from "@/lib/data-service"

export default function DashboardPage() {
  const [mode, setMode] = useState<"realtime" | "historic">("realtime")
  const [selectedTime, setSelectedTime] = useState(new Date())
  const [data, setData] = useState<EnergyData | null>(getInitialMockupData())
  const [isRefreshing, setIsRefreshing] = useState(false)

  // When mode changes, immediately show mockup data
  useEffect(() => {
    if (mode === "realtime") {
      // Show realtime mockup data immediately
      setData(getInitialMockupData())
    } else {
      // Show historic mockup data immediately for the selected time
      setData(getHistoricMockupData(selectedTime))
    }
  }, [mode])

  // When selected time changes in historic mode, immediately show mockup data
  useEffect(() => {
    if (mode === "historic") {
      setData(getHistoricMockupData(selectedTime))
    }
  }, [selectedTime, mode])

  // Fetch data based on the selected mode
  useEffect(() => {
    let isMounted = true
    setIsRefreshing(true)

    const fetchData = async () => {
      try {
        if (mode === "realtime") {
          const currentData = await fetchCurrentData()
          if (isMounted) {
            setData(currentData)
            setSelectedTime(currentData.timestamp)
          }
        } else {
          const historicData = await fetchHistoricData(selectedTime)
          if (isMounted) {
            setData(historicData)
          }
        }
      } catch (error) {
        console.error("Error fetching data:", error)
        // Keep showing the mockup data on error
      } finally {
        if (isMounted) {
          setIsRefreshing(false)
        }
      }
    }

    fetchData()

    // Set up auto-refresh for realtime mode
    let interval: NodeJS.Timeout
    if (mode === "realtime") {
      interval = setInterval(fetchData, 60000) // Refresh every minute
    }

    return () => {
      isMounted = false
      if (interval) clearInterval(interval)
    }
  }, [mode, selectedTime])

  return (
    <div className="flex min-h-screen flex-col">
      <DashboardHeader mode={mode} setMode={setMode} data={data} isRefreshing={isRefreshing} />
      <main className="flex-1 space-y-6 p-6 md:p-8">
        {data ? (
          <>
            <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-3">
              <div className="col-span-full lg:col-span-2">
                <EnergyClockChart data={data} isRefreshing={isRefreshing} />
              </div>
              <div className="space-y-6">
                <Recommendations data={data} isRefreshing={isRefreshing} />
                <EnergyStats data={data} isRefreshing={isRefreshing} />
              </div>
            </div>

            {/* Historic graph slider moved to bottom */}
            <HistoricGraphSlider mode={mode} selectedTime={selectedTime} setSelectedTime={setSelectedTime} />
          </>
        ) : (
          <div className="rounded-lg border p-8 text-center">
            <h3 className="mb-2 text-lg font-medium">No data available</h3>
            <p className="text-muted-foreground">Unable to load energy data. Please try again later.</p>
          </div>
        )}
      </main>
      
    </div>
  )
}
