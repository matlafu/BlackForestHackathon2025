"use client"

import { useState } from "react"
import { Battery, BatteryCharging, BatteryFull, BatteryIcon as BatteryOff, Plus, Power } from "lucide-react"

import { Button } from "@/components/ui/button"
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogHeader,
  DialogTitle,
} from "@/components/ui/dialog"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { Switch } from "@/components/ui/switch"
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs"
import { useToast } from "@/hooks/use-toast"
import type { EnergyData } from "@/lib/data-service"

interface SmartDevice {
  id: string
  name: string
  type: "plug" | "light" | "thermostat" | "other"
  isActive: boolean
  powerUsage: number // in watts
  location: string
}

interface ControlCenterDialogProps {
  open: boolean
  onOpenChange: (open: boolean) => void
  data: EnergyData
  isRefreshing?: boolean
}

export function ControlCenterDialog({ open, onOpenChange, data, isRefreshing = false }: ControlCenterDialogProps) {
  return (
    <Dialog open={open} onOpenChange={onOpenChange}>
      <DialogContent className="sm:max-w-[800px] max-h-[90vh] overflow-y-auto">
        <DialogHeader>
          <DialogTitle className="flex items-center gap-2">
            <Power className="h-5 w-5" />
            Control Center
          </DialogTitle>
          <DialogDescription>Manage your energy devices based on current recommendations</DialogDescription>
        </DialogHeader>
        <ControlCenter data={data} isRefreshing={isRefreshing} />
      </DialogContent>
    </Dialog>
  )
}

interface ControlCenterProps {
  data: EnergyData
  isRefreshing?: boolean
}

function ControlCenter({ data, isRefreshing = false }: ControlCenterProps) {
  const { toast } = useToast()
  const [batteryMode, setBatteryMode] = useState<"auto" | "charge" | "discharge" | "off">("auto")
  const [addDeviceOpen, setAddDeviceOpen] = useState(false)
  const [newDevice, setNewDevice] = useState<Partial<SmartDevice>>({
    name: "",
    type: "plug",
    location: "",
  })

  // Mock smart devices
  const [smartDevices, setSmartDevices] = useState<SmartDevice[]>([
    {
      id: "device-1",
      name: "Living Room Lamp",
      type: "plug",
      isActive: true,
      powerUsage: 60,
      location: "Living Room",
    },
    {
      id: "device-2",
      name: "Kitchen Appliances",
      type: "plug",
      isActive: false,
      powerUsage: 1200,
      location: "Kitchen",
    },
    {
      id: "device-3",
      name: "Office Equipment",
      type: "plug",
      isActive: true,
      powerUsage: 85,
      location: "Office",
    },
  ])

  const currentHour = data.timestamp.getHours()
  const currentSource = data.hourlyRecommendations.find((rec) => rec.hour === currentHour)?.source || "unknown"

  // Get the recommended battery mode based on current energy source
  const getRecommendedBatteryMode = () => {
    switch (currentSource) {
      case "solar-to-battery":
        return "charge"
      case "solar-direct":
        return "off" // Direct solar use, no battery needed
      case "battery":
        return "discharge"
      case "grid":
        return "auto" // Let the system decide
      default:
        return "auto"
    }
  }

  // Get the recommended device state based on current energy source and device power usage
  const getRecommendedDeviceState = (device: SmartDevice) => {
    // High power devices (>500W)
    if (device.powerUsage > 500) {
      switch (currentSource) {
        case "solar-to-battery":
        case "solar-direct":
          return true // Turn on during solar production
        case "battery":
        case "grid":
          return false // Turn off to save energy
        default:
          return device.isActive
      }
    } else {
      // Low power devices
      switch (currentSource) {
        case "grid":
          return device.powerUsage < 100 // Only very low power devices during grid
        default:
          return true // Can be on during other times
      }
    }
  }

  const toggleDevice = (id: string) => {
    setSmartDevices((prev) =>
      prev.map((device) => {
        if (device.id === id) {
          const newState = !device.isActive

          // Show toast notification
          toast({
            title: `${device.name} turned ${newState ? "on" : "off"}`,
            description: `Power usage: ${device.powerUsage}W`,
          })

          return { ...device, isActive: newState }
        }
        return device
      }),
    )
  }

  const changeBatteryMode = (mode: "auto" | "charge" | "discharge" | "off") => {
    setBatteryMode(mode)

    // Show toast notification
    toast({
      title: `Battery mode changed to ${mode}`,
      description: getBatteryModeDescription(mode),
    })
  }

  const getBatteryModeDescription = (mode: string) => {
    switch (mode) {
      case "auto":
        return "System will automatically manage battery usage"
      case "charge":
        return "Battery will prioritize charging from available sources"
      case "discharge":
        return "Battery will be used as primary power source"
      case "off":
        return "Battery is disconnected from the system"
      default:
        return ""
    }
  }

  const getBatteryIcon = () => {
    switch (batteryMode) {
      case "charge":
        return <BatteryCharging className="h-5 w-5" />
      case "discharge":
        return <Battery className="h-5 w-5" />
      case "off":
        return <BatteryOff className="h-5 w-5" />
      default:
        return <BatteryFull className="h-5 w-5" />
    }
  }

  const handleAddDevice = () => {
    if (!newDevice.name) {
      toast({
        title: "Device name required",
        description: "Please enter a name for your device",
      })
      return
    }

    const device: SmartDevice = {
      id: `device-${Date.now()}`,
      name: newDevice.name || "New Device",
      type: (newDevice.type as "plug" | "light" | "thermostat" | "other") || "plug",
      isActive: false,
      powerUsage: 100, // Default power usage
      location: newDevice.location || "Home",
    }

    setSmartDevices((prev) => [...prev, device])
    setNewDevice({ name: "", type: "plug", location: "" })
    setAddDeviceOpen(false)

    toast({
      title: "Device added successfully",
      description: `${device.name} has been added to your smart devices`,
    })
  }

  const recommendedBatteryMode = getRecommendedBatteryMode()

  return (
    <div className="py-4">
      <Tabs defaultValue="devices">
        <TabsList className="mb-4 grid w-full grid-cols-2">
          <TabsTrigger value="devices">Smart Devices</TabsTrigger>
          <TabsTrigger value="battery">Battery Control</TabsTrigger>
        </TabsList>

        <TabsContent value="devices" className="space-y-4">
          <div className="flex items-center justify-between">
            <h3 className="text-sm font-medium">Connected Devices</h3>
            <Button size="sm" variant="outline" onClick={() => setAddDeviceOpen(true)}>
              <Plus className="h-3.5 w-3.5 mr-1" />
              Add Device
            </Button>
          </div>

          <div className="space-y-3">
            {smartDevices.map((device) => {
              const recommended = getRecommendedDeviceState(device)
              return (
                <div
                  key={device.id}
                  className={`flex items-center justify-between rounded-lg border p-3 ${
                    recommended !== device.isActive
                      ? "border-yellow-300 bg-yellow-50 dark:border-yellow-800 dark:bg-yellow-950/30"
                      : ""
                  }`}
                >
                  <div className="space-y-0.5">
                    <div className="flex items-center">
                      <span className="font-medium">{device.name}</span>
                      {recommended !== device.isActive && (
                        <span className="ml-2 text-xs text-yellow-600 dark:text-yellow-400">
                          Recommendation: Turn {recommended ? "on" : "off"}
                        </span>
                      )}
                    </div>
                    <div className="flex items-center text-xs text-muted-foreground">
                      <span>{device.location}</span>
                      <span className="mx-1">•</span>
                      <span>{device.powerUsage}W</span>
                    </div>
                  </div>
                  <div className="flex items-center gap-2">
                    <Switch checked={device.isActive} onCheckedChange={() => toggleDevice(device.id)} />
                    <span className="text-xs font-medium">{device.isActive ? "ON" : "OFF"}</span>
                  </div>
                </div>
              )
            })}

            {smartDevices.length === 0 && (
              <div className="rounded-lg border border-dashed p-6 text-center">
                <h4 className="text-sm font-medium">No devices connected</h4>
                <p className="mt-1 text-xs text-muted-foreground">
                  Add your first smart device to start controlling it
                </p>
                <Button size="sm" variant="outline" className="mt-4" onClick={() => setAddDeviceOpen(true)}>
                  <Plus className="h-3.5 w-3.5 mr-1" />
                  Add Device
                </Button>
              </div>
            )}
          </div>
        </TabsContent>

        <TabsContent value="battery" className="space-y-4">
          <div className="rounded-lg border p-4">
            <div className="flex items-center justify-between">
              <div className="flex items-center gap-2">
                {getBatteryIcon()}
                <h3 className="font-medium">Battery Status</h3>
              </div>
              <div className="text-sm font-medium">{Math.round((data.batteryStorage / 1.5) * 100)}% Charged</div>
            </div>

            <div className="mt-4 h-2 w-full rounded-full bg-muted">
              <div
                className="h-full rounded-full bg-green-500"
                style={{ width: `${Math.round((data.batteryStorage / 1.5) * 100)}%` }}
              />
            </div>

            <div className="mt-6">
              <h4 className="mb-2 text-sm font-medium">Battery Mode</h4>
              <div className="grid grid-cols-2 gap-2 sm:grid-cols-4">
                <Button
                  variant={batteryMode === "auto" ? "default" : "outline"}
                  size="sm"
                  onClick={() => changeBatteryMode("auto")}
                  className="justify-start"
                >
                  <BatteryFull className="h-4 w-4 mr-2" />
                  Auto
                </Button>
                <Button
                  variant={batteryMode === "charge" ? "default" : "outline"}
                  size="sm"
                  onClick={() => changeBatteryMode("charge")}
                  className="justify-start"
                >
                  <BatteryCharging className="h-4 w-4 mr-2" />
                  Charge
                </Button>
                <Button
                  variant={batteryMode === "discharge" ? "default" : "outline"}
                  size="sm"
                  onClick={() => changeBatteryMode("discharge")}
                  className="justify-start"
                >
                  <Battery className="h-4 w-4 mr-2" />
                  Discharge
                </Button>
                <Button
                  variant={batteryMode === "off" ? "default" : "outline"}
                  size="sm"
                  onClick={() => changeBatteryMode("off")}
                  className="justify-start"
                >
                  <BatteryOff className="h-4 w-4 mr-2" />
                  Off
                </Button>
              </div>
            </div>

            {recommendedBatteryMode !== batteryMode && (
              <div className="mt-4 rounded-lg bg-yellow-50 p-3 text-sm dark:bg-yellow-950/30">
                <div className="font-medium text-yellow-800 dark:text-yellow-300">Recommendation</div>
                <p className="mt-1 text-yellow-700 dark:text-yellow-400">
                  Based on current energy conditions, we recommend setting battery mode to{" "}
                  <span className="font-medium">{recommendedBatteryMode}</span>.
                </p>
                <Button
                  size="sm"
                  variant="outline"
                  className="mt-2 bg-yellow-100 hover:bg-yellow-200 dark:bg-yellow-900 dark:hover:bg-yellow-800"
                  onClick={() => changeBatteryMode(recommendedBatteryMode as any)}
                >
                  Apply Recommendation
                </Button>
              </div>
            )}
          </div>

          <div className="rounded-lg border p-4">
            <h3 className="font-medium">Battery Statistics</h3>
            <div className="mt-3 grid grid-cols-2 gap-4">
              <div>
                <div className="text-xs text-muted-foreground">Current Storage</div>
                <div className="text-lg font-medium">{data.batteryStorage.toFixed(1)} kWh</div>
              </div>
              <div>
                <div className="text-xs text-muted-foreground">Capacity</div>
                <div className="text-lg font-medium">1.5 kWh</div>
              </div>
              <div>
                <div className="text-xs text-muted-foreground">Power Output</div>
                <div className="text-lg font-medium">
                  {batteryMode === "discharge" ? "600W" : batteryMode === "off" ? "0W" : "300W"}
                </div>
              </div>
              <div>
                <div className="text-xs text-muted-foreground">Estimated Runtime</div>
                <div className="text-lg font-medium">
                  {batteryMode === "discharge" ? "2.5h" : batteryMode === "off" ? "0h" : "5h"}
                </div>
              </div>
            </div>
          </div>
        </TabsContent>
      </Tabs>

      {/* Add Device Dialog */}
      <Dialog open={addDeviceOpen} onOpenChange={setAddDeviceOpen}>
        <DialogContent>
          <DialogHeader>
            <DialogTitle>Add Smart Device</DialogTitle>
            <DialogDescription>Connect a new smart device to your energy management system.</DialogDescription>
          </DialogHeader>

          <div className="space-y-4 py-2">
            <div className="space-y-2">
              <Label htmlFor="device-name">Device Name</Label>
              <Input
                id="device-name"
                placeholder="Living Room Lamp"
                value={newDevice.name}
                onChange={(e) => setNewDevice({ ...newDevice, name: e.target.value })}
              />
            </div>

            <div className="space-y-2">
              <Label htmlFor="device-type">Device Type</Label>
              <select
                id="device-type"
                className="flex h-10 w-full rounded-md border border-input bg-background px-3 py-2 text-sm ring-offset-background file:border-0 file:bg-transparent file:text-sm file:font-medium placeholder:text-muted-foreground focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:cursor-not-allowed disabled:opacity-50"
                value={newDevice.type}
                onChange={(e) => setNewDevice({ ...newDevice, type: e.target.value as any })}
              >
                <option value="plug">Smart Plug</option>
                <option value="light">Smart Light</option>
                <option value="thermostat">Thermostat</option>
                <option value="other">Other</option>
              </select>
            </div>

            <div className="space-y-2">
              <Label htmlFor="device-location">Location</Label>
              <Input
                id="device-location"
                placeholder="Kitchen, Living Room, etc."
                value={newDevice.location}
                onChange={(e) => setNewDevice({ ...newDevice, location: e.target.value })}
              />
            </div>
          </div>

          <DialogFooter>
            <Button variant="outline" onClick={() => setAddDeviceOpen(false)}>
              Cancel
            </Button>
            <Button onClick={handleAddDevice}>Add Device</Button>
          </DialogFooter>
        </DialogContent>
      </Dialog>
    </div>
  )
}
