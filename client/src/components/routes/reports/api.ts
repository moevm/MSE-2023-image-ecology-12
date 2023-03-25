import { ReportInfo } from "@/types/reports";
import axios from "axios";
import { baseURL } from "@/api";


export function getReportsInfo(): Promise<ReportInfo[]> {  
  return Promise.resolve([
    { id: "1", date: "2023-03-01T12:01:10", anomalies: 3, name: "Лес 1" },
    { id: "2", date: "2023-03-01T12:01:10", anomalies: 2, name: "Лес 2" },
    {
      id: "3",
      date: "2023-03-01T12:01:10",
      anomalies: 1,
      name: "Весенний лес",
    },
    {
      id: "4",
      date: "2023-03-01T12:01:10",
      anomalies: 4,
      name: "Карта Металлостроя",
    },
    { id: "5", date: "2023-03-01T12:01:10", anomalies: 5, name: "Лес 3" },
  ]);
}
