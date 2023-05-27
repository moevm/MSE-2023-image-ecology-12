export interface AnomalyInfo {
  id: string;
  name: string;
  anomalyIndex: string;
  area: number;
  uploadDate: string;
  detectDate: string;
}

export interface AnomalyData {
  reportId: string;
  mapId: string;
  name: string;
  anomalyIndex: string;
  area: number;
  uploadDate: string;
  detectDate: string;
}

export interface AnomaliesMapData {
    name: string,
    color: string,
    polygons: number[][][]
}
