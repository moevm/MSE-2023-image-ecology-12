export interface MapInfo {
  id: number;
  name: string;
  date: string;
  size: number;
  ready: boolean;
}

export interface MapAnomaly {
  id: number;
  name: string;
  area: number;
  coordinates: [number, number];
}
