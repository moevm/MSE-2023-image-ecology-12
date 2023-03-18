import { MapAnomaly } from "@/types/maps";

export interface ReportInfo {
  id: number;
  name: string;
  date: string;
  anomalies: number;
}

export interface ReportData {
  mapId: number;
  anomalies: MapAnomaly[];
}
