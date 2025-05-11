"use client"

import { useState } from "react"
import { Battery, MapPin, Save, SunIcon } from "lucide-react"

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
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs"
import { useToast } from "@/hooks/use-toast"

interface SettingsModalProps {
  open: boolean
  onOpenChange: (open: boolean) => void
}

interface SystemSettings {
  pvPower: number
  batteryCapacity: number
  location: string
}

export function SettingsModal({ open, onOpenChange }: SettingsModalProps) {
  const { toast } = useToast()
  const [settings, setSettings] = useState<SystemSettings>({
    pvPower: 600, // Default value in Watts
    batteryCapacity: 1.5, // Default value in kWh
    location: "", // Default empty
  })

  const handleSave = () => {
    // In a real application, this would save to a database or localStorage
    console.log("Saving settings:", settings)

    // Show success toast
    toast({
      title: "Settings saved",
      description: "Your system settings have been updated successfully.",
    })

    // Close the modal
    onOpenChange(false)
  }

  return (
    <Dialog open={open} onOpenChange={onOpenChange}>
      <DialogContent className="sm:max-w-[500px]">
        <DialogHeader>
          <DialogTitle>System Settings</DialogTitle>
          <DialogDescription>
            Configure your BalkonSolar system parameters. These settings affect energy calculations and recommendations.
          </DialogDescription>
        </DialogHeader>

        <Tabs defaultValue="system" className="mt-4">
          <TabsList className="grid w-full grid-cols-2">
            <TabsTrigger value="system">System</TabsTrigger>
            <TabsTrigger value="location">Location</TabsTrigger>
          </TabsList>

          <TabsContent value="system" className="space-y-4 pt-4">
            <div className="space-y-2">
              <Label htmlFor="pv-power" className="flex items-center gap-2">
                <SunIcon className="h-4 w-4 text-yellow-500" />
                PV Power (Watts)
              </Label>
              <Input
                id="pv-power"
                type="number"
                value={settings.pvPower}
                onChange={(e) => setSettings({ ...settings, pvPower: Number(e.target.value) })}
                min="0"
                step="10"
              />
              <p className="text-xs text-muted-foreground">The maximum power output of your solar panels in Watts.</p>
            </div>

            <div className="space-y-2">
              <Label htmlFor="battery-capacity" className="flex items-center gap-2">
                <Battery className="h-4 w-4 text-green-500" />
                Battery Capacity (kWh)
              </Label>
              <Input
                id="battery-capacity"
                type="number"
                value={settings.batteryCapacity}
                onChange={(e) => setSettings({ ...settings, batteryCapacity: Number(e.target.value) })}
                min="0"
                step="0.1"
              />
              <p className="text-xs text-muted-foreground">
                The total energy storage capacity of your battery in kilowatt-hours.
              </p>
            </div>
          </TabsContent>

          <TabsContent value="location" className="space-y-4 pt-4">
            <div className="space-y-2">
              <Label htmlFor="location" className="flex items-center gap-2">
                <MapPin className="h-4 w-4 text-red-500" />
                Address
              </Label>
              <Input
                id="location"
                value={settings.location}
                onChange={(e) => setSettings({ ...settings, location: e.target.value })}
                placeholder="Enter your address"
              />
              <p className="text-xs text-muted-foreground">
                Your location is used to calculate optimal solar production times based on local weather and sunlight
                data.
              </p>
            </div>

            <div className="rounded-md border p-4 bg-muted/50">
              <h4 className="text-sm font-medium mb-2">Why we need your location</h4>
              <p className="text-xs text-muted-foreground">
                Your location helps us provide more accurate solar production estimates and energy usage recommendations
                based on local weather patterns, sunrise/sunset times, and seasonal variations.
              </p>
            </div>
          </TabsContent>
        </Tabs>

        <DialogFooter>
          <Button variant="outline" onClick={() => onOpenChange(false)}>
            Cancel
          </Button>
          <Button onClick={handleSave} className="gap-2">
            <Save className="h-4 w-4" />
            Save Changes
          </Button>
        </DialogFooter>
      </DialogContent>
    </Dialog>
  )
}
