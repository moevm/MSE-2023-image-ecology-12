import { MapAnomaly } from "@/types/maps";

export interface ReportInfo {
  id: string;
  anomalyIndex: string;
  name: string;
  date: string;
  anomalies: number;
}

export interface ReportData {
  mapId: string;
  anomalies: MapAnomaly[];
}
