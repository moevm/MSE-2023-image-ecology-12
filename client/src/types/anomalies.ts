export interface AnomalyInfo {
  id: string;
  name: string;
  area: number;
  uploadDate: string;
  detectDate: string;
}

export interface AnomalyData {
  reportId: string;
  mapId: string;
  name: string;
  area: number;
  uploadDate: string;
  detectDate: string;
  coordinates: [number, number];
}
