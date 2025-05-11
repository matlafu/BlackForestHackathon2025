export interface EnergyData {
  timestamp: Date;
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
    id: number;
    timestamp: string;
    value: number;
  }>;
} 