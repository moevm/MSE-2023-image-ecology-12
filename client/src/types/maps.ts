export interface MapInfo {
  id: string;
  name: string;
  date: string;
  size: number;
  ready: boolean;
}

export interface MapAnomaly {
  id: string;
  name: string;
  area: number;
  coordinates: [number, number];
}

export interface MapData {
  reportId?: string;
  anomalies?: MapAnomaly[];
}
