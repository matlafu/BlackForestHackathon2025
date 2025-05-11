/*
  constants.ts for the Balkonsolar Dashboard
  - Defines table metadata (id, display name, color) for use in charts and UI
*/
export const TABLES = [
  { id: 'solar_output', name: 'Solarproduktion', color: '#f59e0b' },
  // { id: 'battery_storage_status', name: 'Batteriestatus', color: '#10b981' },
  { id: 'grid_usage', name: 'Netznutzung', color: '#3b82f6' },
  // { id: 'output_algorithm', name: 'Algorithmus-Output', color: '#8b5cf6' }
] as const;
