export interface ReportInfo {
  id: number;
  date: string;
  anomalies: number;
}

export interface MapObject {
  name: string;
  coordinates: [number, number];
}

export interface MapObjectsGroup {
  name: string;
  objects: MapObject[];
}

export interface Report {
  id: number;
  groups: MapObjectsGroup[];
}
