// This is a mock data service that would normally fetch data from a database
// In a real application, you would replace this with actual API calls

import { TABLES } from './constants';

// Types for our data
export interface EnergyData {
  timestamp: Date;
  solarProduction: number;
  batteryStorage: number;
  gridUsage: number;
  totalConsumption: number;
  hourlyRecommendations: Array<{ hour: number; source: string }>;
  powerFlow: {
    solarToHome: number;
    solarToBattery: number;
    batteryToHome: number;
    gridToHome: number;
    batteryToGrid: number;
  };
  solar_output: Array<{
    id: number;
    timestamp: string;
    value: number;
  }>;
  battery_storage_status: Array<{
    id: number;
    timestamp: string;
    value: number;
  }>;
  grid_usage: Array<{
    id: number;
    timestamp: string;
    value: number;
  }>;
  output_algorithm: Array<{
    id?: number;
    timestamp: string;
    suggested_state: string;
    value: number;
    usage: number;
  }>;
}

export interface PowerFlow {
  solarToHome: number
  solarToBattery: number
  batteryToHome: number
  gridToHome: number
  batteryToGrid: number
}

export interface HourlyRecommendation {
  hour: number
  source: "solar-to-battery" | "solar-direct" | "battery" | "grid"
  label: string
}

// Timeline data interface for 24-hour charts
export interface TimelineDataPoint {
  hour: number
  solarProduction: number
  batteryStorage: number
  gridUsage: number
  consumption: number
}

// Original hourly recommendations (used for realtime mode)
export const originalHourlyRecommendations: HourlyRecommendation[] = [
  { hour: 0, source: "grid", label: "Grid" },
  { hour: 1, source: "grid", label: "Grid" },
  { hour: 2, source: "grid", label: "Grid" },
  { hour: 3, source: "grid", label: "Grid" },
  { hour: 4, source: "grid", label: "Grid" },
  { hour: 5, source: "grid", label: "Grid" },
  { hour: 6, source: "solar-to-battery", label: "Charge" },
  { hour: 7, source: "solar-to-battery", label: "Charge" },
  { hour: 8, source: "solar-to-battery", label: "Charge" },
  { hour: 9, source: "solar-to-battery", label: "Charge" },
  { hour: 10, source: "solar-to-battery", label: "Charge" },
  { hour: 11, source: "solar-to-battery", label: "Charge" },
  { hour: 12, source: "solar-to-battery", label: "Charge" },
  { hour: 13, source: "solar-to-battery", label: "Charge" },
  { hour: 14, source: "solar-to-battery", label: "Charge" },
  { hour: 15, source: "solar-to-battery", label: "Charge" },
  { hour: 16, source: "solar-direct", label: "Solar" },
  { hour: 17, source: "solar-direct", label: "Solar" },
  { hour: 18, source: "battery", label: "Battery" },
  { hour: 19, source: "battery", label: "Battery" },
  { hour: 20, source: "battery", label: "Battery" },
  { hour: 21, source: "battery", label: "Battery" },
  { hour: 22, source: "grid", label: "Grid" },
  { hour: 23, source: "grid", label: "Grid" },
]

// Original power flow data (used for realtime mode)
export const originalPowerFlow: PowerFlow = {
  solarToHome: 0.6,
  solarToBattery: 0.4,
  batteryToHome: 0,
  gridToHome: 0,
  batteryToGrid: 0,
}

// Predefined hourly recommendation patterns for different days
const hourlyRecommendationPatterns = [
  // Pattern 0: Sunny day with good battery (original pattern)
  originalHourlyRecommendations,

  // Pattern 1: Cloudy morning, sunny afternoon
  [
    { hour: 0, source: "grid", label: "Grid" },
    { hour: 1, source: "grid", label: "Grid" },
    { hour: 2, source: "grid", label: "Grid" },
    { hour: 3, source: "grid", label: "Grid" },
    { hour: 4, source: "grid", label: "Grid" },
    { hour: 5, source: "grid", label: "Grid" },
    { hour: 6, source: "grid", label: "Grid" },
    { hour: 7, source: "grid", label: "Grid" },
    { hour: 8, source: "grid", label: "Grid" },
    { hour: 9, source: "solar-direct", label: "Solar" },
    { hour: 10, source: "solar-direct", label: "Solar" },
    { hour: 11, source: "solar-to-battery", label: "Charge" },
    { hour: 12, source: "solar-to-battery", label: "Charge" },
    { hour: 13, source: "solar-to-battery", label: "Charge" },
    { hour: 14, source: "solar-to-battery", label: "Charge" },
    { hour: 15, source: "solar-to-battery", label: "Charge" },
    { hour: 16, source: "solar-direct", label: "Solar" },
    { hour: 17, source: "solar-direct", label: "Solar" },
    { hour: 18, source: "battery", label: "Battery" },
    { hour: 19, source: "battery", label: "Battery" },
    { hour: 20, source: "battery", label: "Battery" },
    { hour: 21, source: "grid", label: "Grid" },
    { hour: 22, source: "grid", label: "Grid" },
    { hour: 23, source: "grid", label: "Grid" },
  ],

  // Pattern 2: Rainy day, mostly grid
  [
    { hour: 0, source: "grid", label: "Grid" },
    { hour: 1, source: "grid", label: "Grid" },
    { hour: 2, source: "grid", label: "Grid" },
    { hour: 3, source: "grid", label: "Grid" },
    { hour: 4, source: "grid", label: "Grid" },
    { hour: 5, source: "grid", label: "Grid" },
    { hour: 6, source: "grid", label: "Grid" },
    { hour: 7, source: "grid", label: "Grid" },
    { hour: 8, source: "grid", label: "Grid" },
    { hour: 9, source: "grid", label: "Grid" },
    { hour: 10, source: "grid", label: "Grid" },
    { hour: 11, source: "solar-direct", label: "Solar" },
    { hour: 12, source: "solar-direct", label: "Solar" },
    { hour: 13, source: "solar-direct", label: "Solar" },
    { hour: 14, source: "grid", label: "Grid" },
    { hour: 15, source: "grid", label: "Grid" },
    { hour: 16, source: "grid", label: "Grid" },
    { hour: 17, source: "grid", label: "Grid" },
    { hour: 18, source: "battery", label: "Battery" },
    { hour: 19, source: "battery", label: "Battery" },
    { hour: 20, source: "grid", label: "Grid" },
    { hour: 21, source: "grid", label: "Grid" },
    { hour: 22, source: "grid", label: "Grid" },
    { hour: 23, source: "grid", label: "Grid" },
  ],

  // Pattern 3: Very sunny day, lots of battery charging
  [
    { hour: 0, source: "battery", label: "Battery" },
    { hour: 1, source: "battery", label: "Battery" },
    { hour: 2, source: "grid", label: "Grid" },
    { hour: 3, source: "grid", label: "Grid" },
    { hour: 4, source: "grid", label: "Grid" },
    { hour: 5, source: "grid", label: "Grid" },
    { hour: 6, source: "solar-direct", label: "Solar" },
    { hour: 7, source: "solar-direct", label: "Solar" },
    { hour: 8, source: "solar-to-battery", label: "Charge" },
    { hour: 9, source: "solar-to-battery", label: "Charge" },
    { hour: 10, source: "solar-to-battery", label: "Charge" },
    { hour: 11, source: "solar-to-battery", label: "Charge" },
    { hour: 12, source: "solar-to-battery", label: "Charge" },
    { hour: 13, source: "solar-to-battery", label: "Charge" },
    { hour: 14, source: "solar-to-battery", label: "Charge" },
    { hour: 15, source: "solar-to-battery", label: "Charge" },
    { hour: 16, source: "solar-to-battery", label: "Charge" },
    { hour: 17, source: "solar-direct", label: "Solar" },
    { hour: 18, source: "battery", label: "Battery" },
    { hour: 19, source: "battery", label: "Battery" },
    { hour: 20, source: "battery", label: "Battery" },
    { hour: 21, source: "battery", label: "Battery" },
    { hour: 22, source: "battery", label: "Battery" },
    { hour: 23, source: "battery", label: "Battery" },
  ],

  // Pattern 4: Partly cloudy, good battery management
  [
    { hour: 0, source: "grid", label: "Grid" },
    { hour: 1, source: "grid", label: "Grid" },
    { hour: 2, source: "grid", label: "Grid" },
    { hour: 3, source: "grid", label: "Grid" },
    { hour: 4, source: "grid", label: "Grid" },
    { hour: 5, source: "grid", label: "Grid" },
    { hour: 6, source: "solar-direct", label: "Solar" },
    { hour: 7, source: "solar-direct", label: "Solar" },
    { hour: 8, source: "solar-direct", label: "Solar" },
    { hour: 9, source: "solar-to-battery", label: "Charge" },
    { hour: 10, source: "grid", label: "Grid" },
    { hour: 11, source: "solar-to-battery", label: "Charge" },
    { hour: 12, source: "solar-to-battery", label: "Charge" },
    { hour: 13, source: "grid", label: "Grid" },
    { hour: 14, source: "solar-to-battery", label: "Charge" },
    { hour: 15, source: "solar-direct", label: "Solar" },
    { hour: 16, source: "solar-direct", label: "Solar" },
    { hour: 17, source: "grid", label: "Grid" },
    { hour: 18, source: "battery", label: "Battery" },
    { hour: 19, source: "battery", label: "Battery" },
    { hour: 20, source: "battery", label: "Battery" },
    { hour: 21, source: "grid", label: "Grid" },
    { hour: 22, source: "grid", label: "Grid" },
    { hour: 23, source: "grid", label: "Grid" },
  ],

  // Pattern 5: Morning clouds, afternoon sun, evening grid
  [
    { hour: 0, source: "grid", label: "Grid" },
    { hour: 1, source: "grid", label: "Grid" },
    { hour: 2, source: "grid", label: "Grid" },
    { hour: 3, source: "grid", label: "Grid" },
    { hour: 4, source: "grid", label: "Grid" },
    { hour: 5, source: "grid", label: "Grid" },
    { hour: 6, source: "grid", label: "Grid" },
    { hour: 7, source: "grid", label: "Grid" },
    { hour: 8, source: "grid", label: "Grid" },
    { hour: 9, source: "grid", label: "Grid" },
    { hour: 10, source: "solar-direct", label: "Solar" },
    { hour: 11, source: "solar-direct", label: "Solar" },
    { hour: 12, source: "solar-to-battery", label: "Charge" },
    { hour: 13, source: "solar-to-battery", label: "Charge" },
    { hour: 14, source: "solar-to-battery", label: "Charge" },
    { hour: 15, source: "solar-direct", label: "Solar" },
    { hour: 16, source: "solar-direct", label: "Solar" },
    { hour: 17, source: "solar-direct", label: "Solar" },
    { hour: 18, source: "grid", label: "Grid" },
    { hour: 19, source: "grid", label: "Grid" },
    { hour: 20, source: "battery", label: "Battery" },
    { hour: 21, source: "battery", label: "Battery" },
    { hour: 22, source: "grid", label: "Grid" },
    { hour: 23, source: "grid", label: "Grid" },
  ],
]

// Predefined power flow patterns for different sources
const powerFlowPatterns: Record<string, PowerFlow> = {
  "solar-to-battery": {
    solarToHome: 0.3,
    solarToBattery: 0.7,
    batteryToHome: 0,
    gridToHome: 0.1,
    batteryToGrid: 0,
  },
  "solar-direct": {
    solarToHome: 0.8,
    solarToBattery: 0,
    batteryToHome: 0,
    gridToHome: 0.1,
    batteryToGrid: 0,
  },
  battery: {
    solarToHome: 0,
    solarToBattery: 0,
    batteryToHome: 0.8,
    gridToHome: 0.1,
    batteryToGrid: 0,
  },
  grid: {
    solarToHome: 0,
    solarToBattery: 0,
    batteryToHome: 0,
    gridToHome: 0.9,
    batteryToGrid: 0,
  },
}

// Helper function to generate historical data points
function generateHistoricalDataPoints(baseValue: number, hours: number = 24, isAlgorithm: boolean = false): Array<any> {
  const data = [];
  const now = new Date();
  now.setMinutes(0, 0, 0); // Runde auf volle Stunden
  
  const states = ["Charge Battery", "Use Grid", "power the household from solar", "Mixed"];
  
  for (let i = 0; i < hours; i++) {
    // Berechne den Zeitstempel für jede Stunde, beginnend von 24 Stunden vor jetzt
    const time = new Date(now.getTime());
    time.setHours(time.getHours() - (hours - 1 - i));
    
    const hourOfDay = time.getHours();
    
    // Add daily pattern variation
    let multiplier = 1;
    if (hourOfDay >= 6 && hourOfDay <= 18) { // Daytime hours
      // Create a bell curve peaking at noon
      multiplier = 1 + Math.sin((hourOfDay - 6) * Math.PI / 12);
    } else { // Nighttime hours
      multiplier = 0.5;
    }
    
    // Add some random variation
    const randomFactor = 0.8 + Math.random() * 0.4;
    
    if (isAlgorithm) {
      // Für output_algorithm, wähle einen Zustand basierend auf der Tageszeit
      let suggested_state;
      if (hourOfDay >= 6 && hourOfDay <= 10) {
        suggested_state = "Charge Battery";
      } else if (hourOfDay >= 11 && hourOfDay <= 14) {
        suggested_state = "power the household from solar";
      } else if (hourOfDay >= 15 && hourOfDay <= 19) {
        suggested_state = "Mixed";
      } else {
        suggested_state = "Use Grid";
      }
      
      // Berechne einen realistischen Verbrauchswert basierend auf der Tageszeit
      const baseUsage = 0.8; // Grundlast
      let usageMultiplier = 1.0;
      
      // Höherer Verbrauch morgens und abends
      if (hourOfDay >= 6 && hourOfDay <= 9) { // Morgenspitze
        usageMultiplier = 1.5;
      } else if (hourOfDay >= 17 && hourOfDay <= 22) { // Abendspitze
        usageMultiplier = 1.8;
      } else if (hourOfDay >= 23 || hourOfDay <= 5) { // Nachts
        usageMultiplier = 0.6;
      }
      
      data.push({
        id: i + 1,
        timestamp: time.toISOString(),
        suggested_state,
        value: baseValue * multiplier * randomFactor,
        usage: baseUsage * usageMultiplier * randomFactor
      });
    } else {
      data.push({
        id: i + 1,
        timestamp: time.toISOString(),
        value: baseValue * multiplier * randomFactor
      });
    }
  }
  
  return data;
}

// Get initial mockup data for realtime mode (instant)
export function getInitialMockupData(): EnergyData {
  const now = new Date()
  const currentHour = now.getHours()

  // Get the recommendation for the current hour
  const currentRecommendation = originalHourlyRecommendations.find((rec) => rec.hour === currentHour) || {
    hour: currentHour,
    source: "grid",
    label: "Grid",
  }

  return {
    timestamp: now,
    solarProduction: 2.4,
    batteryStorage: 1.7,
    gridUsage: 0.8,
    totalConsumption: 3.1,
    solar_output: generateHistoricalDataPoints(2.4),
    battery_storage_status: generateHistoricalDataPoints(1.7),
    grid_usage: generateHistoricalDataPoints(0.8),
    output_algorithm: generateHistoricalDataPoints(1.0, 24, true),
    hourlyRecommendations: originalHourlyRecommendations,
    powerFlow: originalPowerFlow,
  }
}

// Get historic mockup data for a specific time (instant)
export function getHistoricMockupData(time: Date): EnergyData {
  const hour = time.getHours()

  // Select a pattern based on the date
  const patternIndex = (time.getDate() + time.getMonth() * 31) % hourlyRecommendationPatterns.length
  const hourlyRecommendations = hourlyRecommendationPatterns[patternIndex]

  // Get the recommendation for the current hour
  const currentRecommendation = hourlyRecommendations.find((rec) => rec.hour === hour) || {
    hour,
    source: "grid",
    label: "Grid",
  }

  // Get the power flow for the current recommendation
  const powerFlow = { ...powerFlowPatterns[currentRecommendation.source] }

  // Generate energy stats based on the current recommendation
  let solarProduction = 0
  let batteryStorage = 0
  let gridUsage = 0
  let totalConsumption = 0

  switch (currentRecommendation.source) {
    case "solar-to-battery":
      solarProduction = 2.0
      batteryStorage = 1.5
      gridUsage = 0.1
      totalConsumption = 1.2
      break
    case "solar-direct":
      solarProduction = 1.8
      batteryStorage = 1.0
      gridUsage = 0.2
      totalConsumption = 1.5
      break
    case "battery":
      solarProduction = 0.3
      batteryStorage = 1.8
      gridUsage = 0.2
      totalConsumption = 1.4
      break
    case "grid":
    default:
      solarProduction = 0.1
      batteryStorage = 0.8
      gridUsage = 1.0
      totalConsumption = 1.2
      break
  }

  return {
    timestamp: time,
    solarProduction,
    batteryStorage,
    gridUsage,
    totalConsumption,
    solar_output: generateHistoricalDataPoints(solarProduction),
    battery_storage_status: generateHistoricalDataPoints(batteryStorage),
    grid_usage: generateHistoricalDataPoints(gridUsage),
    output_algorithm: generateHistoricalDataPoints(totalConsumption, 24, true),
    hourlyRecommendations: mapAlgorithmOutputToRecommendations(generateHistoricalDataPoints(totalConsumption, 24, true)),
    powerFlow,
  }
}

// Fetch current data (realtime mode)
export async function fetchCurrentData(): Promise<EnergyData> {
  try {
    const now = new Date();
    now.setMinutes(0, 0, 0); // Round to current hour

    // Fetch data for each table
    const [solarOutput, batteryStatus, gridUsage, outputAlgorithm] = await Promise.all([
      fetch(`/api/energy?table=solar_output&limit=24`).then(res => res.json()),
      fetch(`/api/energy?table=battery_storage_status&limit=24`).then(res => res.json()),
      fetch(`/api/energy?table=grid_usage&limit=24`).then(res => res.json()),
      fetch(`/api/energy?table=output_algorithm&limit=24`).then(res => res.json())
    ]);

    console.log('API Antwort für output_algorithm:', outputAlgorithm);

    // Stelle sicher, dass die Algorithmus-Ausgabe das richtige Format hat
    const formattedOutputAlgorithm = outputAlgorithm.map((entry: any) => ({
      id: entry.id || undefined,
      timestamp: entry.timestamp,
      suggested_state: entry.suggested_state || entry.grid_state || 'Use Grid', // Fallback auf grid_state oder 'Use Grid'
      value: entry.value || 0,
      usage: entry.usage || 0
    }));

    console.log('Formatierte Algorithmus-Ausgabe:', formattedOutputAlgorithm);

    // Find the current values
    const findCurrentValue = (data: any[]) => {
      const currentHourData = data.find(entry => {
        const entryTime = new Date(entry.timestamp);
        return entryTime.getHours() === now.getHours();
      });
      return currentHourData?.value || 0;
    };

    // Für Battery Storage den neuesten Wert verwenden
    const findLatestBatteryValue = (data: any[]) => {
      if (!data || data.length === 0) return 0;
      const maxTimestamp = Math.max(...data.map(entry => new Date(entry.timestamp).getTime()));
      const latestEntry = data.find(entry => new Date(entry.timestamp).getTime() === maxTimestamp);
      // Konvertiere den Wert in kWh (der Wert kommt als Prozent)
      const batteryCapacityKWh = 1.5; // Maximale Kapazität in kWh
      return (latestEntry?.value || 0) * batteryCapacityKWh / 100;
    };

    const currentSolarProduction = findCurrentValue(solarOutput);
    const currentBatteryStorage = findLatestBatteryValue(batteryStatus);
    const currentGridUsage = findCurrentValue(gridUsage);
    const currentTotalConsumption = currentSolarProduction + currentGridUsage;

    // Calculate power flow based on current values
    const powerFlow = {
      solarToHome: Math.max(0, currentSolarProduction * 0.7),
      solarToBattery: Math.max(0, currentSolarProduction * 0.3),
      batteryToHome: Math.max(0, currentBatteryStorage * 0.2),
      gridToHome: Math.max(0, currentGridUsage),
      batteryToGrid: Math.max(0, currentBatteryStorage * 0.1)
    };

    // Map algorithm output to hourly recommendations
    const hourlyRecommendations = mapAlgorithmOutputToRecommendations(formattedOutputAlgorithm);

    // Return the combined data
    return {
      timestamp: now,
      solarProduction: currentSolarProduction,
      batteryStorage: currentBatteryStorage,
      gridUsage: currentGridUsage,
      totalConsumption: currentTotalConsumption,
      solar_output: solarOutput,
      battery_storage_status: batteryStatus,
      grid_usage: gridUsage,
      output_algorithm: formattedOutputAlgorithm,
      hourlyRecommendations,
      powerFlow
    };
  } catch (error) {
    console.error('Fehler beim Abrufen der Daten:', error);
    throw error;
  }
}

// Fetch historic data for a specific time
export async function fetchHistoricData(time: Date): Promise<EnergyData> {
  try {
    // Convert the time to ISO string for the API
    const timestamp = time.toISOString();
    
    // Fetch data for each table around the specified time
    const [solarOutput, batteryStatus, gridUsage, outputAlgorithm] = await Promise.all([
      fetch(`/api/energy?table=solar_output&timestamp=${timestamp}&limit=24`).then(res => res.json()),
      fetch(`/api/energy?table=battery_storage_status&timestamp=${timestamp}&limit=24`).then(res => res.json()),
      fetch(`/api/energy?table=grid_usage&timestamp=${timestamp}&limit=24`).then(res => res.json()),
      fetch(`/api/energy?table=output_algorithm&timestamp=${timestamp}&limit=24`).then(res => res.json())
    ]);

    console.log('Historische API Antwort für output_algorithm:', outputAlgorithm);

    // Stelle sicher, dass die Algorithmus-Ausgabe das richtige Format hat
    const formattedOutputAlgorithm = outputAlgorithm.map((entry: any) => ({
      id: entry.id || undefined,
      timestamp: entry.timestamp,
      suggested_state: entry.suggested_state || entry.grid_state || 'Use Grid', // Fallback auf grid_state oder 'Use Grid'
      value: entry.value || 0,
      usage: entry.usage || 0
    }));

    console.log('Formatierte historische Algorithmus-Ausgabe:', formattedOutputAlgorithm);

    // Find the closest data points to the requested time
    const findClosestValue = (data: any[]) => {
      return data.reduce((prev, curr) => {
        const prevDiff = Math.abs(new Date(prev.timestamp).getTime() - time.getTime());
        const currDiff = Math.abs(new Date(curr.timestamp).getTime() - time.getTime());
        return currDiff < prevDiff ? curr : prev;
      });
    };

    // Für Battery Storage den neuesten Wert bis zum gewählten Zeitpunkt verwenden
    const findLatestBatteryValue = (data: any[]) => {
      if (!data || data.length === 0) return { value: 0 };
      const validData = data.filter(entry => new Date(entry.timestamp) <= time);
      if (validData.length === 0) return { value: 0 };
      const maxTimestamp = Math.max(...validData.map(entry => new Date(entry.timestamp).getTime()));
      const latestEntry = validData.find(entry => new Date(entry.timestamp).getTime() === maxTimestamp);
      // Konvertiere den Wert in kWh (der Wert kommt als Prozent)
      const batteryCapacityKWh = 1.5; // Maximale Kapazität in kWh
      return { value: ((latestEntry?.value || 0) * batteryCapacityKWh / 100) };
    };

    const currentSolarProduction = findClosestValue(solarOutput).value;
    const currentBatteryStorage = findLatestBatteryValue(batteryStatus).value;
    const currentGridUsage = findClosestValue(gridUsage).value;
    const currentTotalConsumption = currentSolarProduction + currentGridUsage;

    // Calculate power flow based on historic values
    const powerFlow = {
      solarToHome: Math.max(0, currentSolarProduction * 0.7),
      solarToBattery: Math.max(0, currentSolarProduction * 0.3),
      batteryToHome: Math.max(0, currentBatteryStorage * 0.2),
      gridToHome: Math.max(0, currentGridUsage),
      batteryToGrid: Math.max(0, currentBatteryStorage * 0.1)
    };

    // Map algorithm output to hourly recommendations
    const hourlyRecommendations = mapAlgorithmOutputToRecommendations(formattedOutputAlgorithm);

    return {
      timestamp: time,
      solarProduction: currentSolarProduction,
      batteryStorage: currentBatteryStorage,
      gridUsage: currentGridUsage,
      totalConsumption: currentTotalConsumption,
      solar_output: solarOutput,
      battery_storage_status: batteryStatus,
      grid_usage: gridUsage,
      output_algorithm: formattedOutputAlgorithm,
      hourlyRecommendations,
      powerFlow
    };
  } catch (error) {
    console.error('Fehler beim Abrufen der historischen Daten:', error);
    throw error;
  }
}

// Generate 24-hour timeline data
export function generate24HourData(): TimelineDataPoint[] {
  return Array.from({ length: 24 }, (_, hour) => {
    // Simuliere einen typischen Tagesverlauf
    const isDaytime = hour >= 6 && hour <= 18;
    const isPeakSolar = hour >= 10 && hour <= 14;
    const isEveningPeak = hour >= 18 && hour <= 21;

    // Grundwerte
    let solarProduction = 0;
    let batteryStorage = 2.0;
    let gridUsage = 0.5;
    let consumption = 1.0;

    // Anpassen der Werte basierend auf der Tageszeit
    if (isDaytime) {
      if (isPeakSolar) {
        solarProduction = 4.0 + Math.random() * 0.5;
        gridUsage = 0.1;
        batteryStorage = 3.0;
      } else {
        solarProduction = 2.0 + Math.random() * 0.5;
        gridUsage = 0.3;
        batteryStorage = 2.5;
      }
    }

    if (isEveningPeak) {
      consumption = 2.5 + Math.random() * 0.5;
      gridUsage = 1.0;
      batteryStorage = 1.5;
    }

    return {
      hour,
      solarProduction,
      batteryStorage,
      gridUsage,
      consumption
    };
  });
}

// Generate historic battery data for the slider
export function generateHistoricBatteryData(): Array<{ time: Date; level: number }> {
  const data: Array<{ time: Date; level: number }> = [];
  const now = new Date();
  now.setMinutes(0, 0, 0); // Runde auf volle Stunden

  for (let i = 0; i < 24; i++) {
    const time = new Date(now.getTime() - (23 - i) * 60 * 60 * 1000);
    const hour = time.getHours();
    
    // Simuliere einen typischen Tagesverlauf des Batteriestands
    let level = 0.5; // Grundniveau

    // Nachts: niedrigerer Stand
    if (hour >= 0 && hour < 6) {
      level = 0.3 + Math.random() * 0.2;
    }
    // Morgens: Laden durch Solar
    else if (hour >= 6 && hour < 12) {
      level = 0.4 + ((hour - 6) / 6) * 0.5 + Math.random() * 0.1;
    }
    // Mittags: Höchststand
    else if (hour >= 12 && hour < 15) {
      level = 0.8 + Math.random() * 0.2;
    }
    // Nachmittags: Langsam sinkend
    else if (hour >= 15 && hour < 18) {
      level = 0.7 - ((hour - 15) / 3) * 0.2 + Math.random() * 0.1;
    }
    // Abends: Nutzung der Batterie
    else if (hour >= 18 && hour < 22) {
      level = 0.5 - ((hour - 18) / 4) * 0.3 + Math.random() * 0.1;
    }
    // Spätnachts: Niedrigster Stand
    else {
      level = 0.2 + Math.random() * 0.1;
    }

    data.push({ time, level: Math.min(1, Math.max(0, level)) });
  }

  return data;
}

// Mapping function to convert algorithm output to clock recommendations
export function mapAlgorithmOutputToRecommendations(outputAlgorithm: Array<{ timestamp: string; suggested_state: string; value: number }>): Array<{ hour: number; source: string }> {
  console.log('Rohe Algorithmus-Ausgabe:', outputAlgorithm);
  
  const recommendations: Array<{ hour: number; source: string }> = [];
  
  // Group by hour and take the most common suggestion for each hour
  const hourlyGroups = new Map<number, { [key: string]: number }>();
  
  outputAlgorithm.forEach(entry => {
    const date = new Date(entry.timestamp);
    const hour = date.getHours();
    
    if (!hourlyGroups.has(hour)) {
      hourlyGroups.set(hour, {});
    }
    
    const hourGroup = hourlyGroups.get(hour)!;
    // Normalisiere den Zustand zu Kleinbuchstaben für den Vergleich
    const state = entry.suggested_state?.toLowerCase() || 'use grid';
    console.log(`Verarbeite Eintrag - Stunde: ${hour}, Original Zustand: ${entry.suggested_state}, Normalisiert: ${state}`);
    hourGroup[state] = (hourGroup[state] || 0) + 1;
  });
  
  console.log('Gruppierte Daten nach Stunden:', Object.fromEntries(hourlyGroups));
  
  // Convert algorithm states to clock sources
  for (let hour = 0; hour < 24; hour++) {
    const hourGroup = hourlyGroups.get(hour) || {};
    let mostCommonState = "use grid"; // Default state
    let maxCount = 0;
    
    console.log(`\nAnalysiere Stunde ${hour}:`, hourGroup);
    
    for (const [state, count] of Object.entries(hourGroup)) {
      if (count > maxCount) {
        maxCount = count;
        mostCommonState = state;
      }
    }
    
    // Map algorithm states to clock sources
    let source: string;
    switch (mostCommonState) {
      case "charge battery":
        source = "solar-to-battery";
        break;
      case "use grid":
        source = "grid";
        break;
      case "power the household from solar":
        source = "solar-direct";
        break;
      case "mixed":
        source = "battery";
        break;
      default:
        console.log(`Unbekannter Zustand für Stunde ${hour}: "${mostCommonState}"`);
        source = "grid";
    }
    
    console.log(`Stunde ${hour}: Häufigster Zustand = "${mostCommonState}" -> Quelle = "${source}"`);
    
    recommendations.push({ hour, source });
  }
  
  console.log('Finale Empfehlungen:', recommendations);
  
  return recommendations;
}
