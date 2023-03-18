export interface AnomalyInfo {
  id: number;
  name: string;
  area: number;
  uploadDate: string;
  detectDate: string;
}

export interface AnomalyData {
  reportId: number;
  mapId: number;
  name: string;
  area: number;
  uploadDate: string;
  detectDate: string;
  coordinates: [number, number];
}
