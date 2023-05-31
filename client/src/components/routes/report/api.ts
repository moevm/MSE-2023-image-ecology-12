import { ReportData } from "@/types/reports";
import axios from "axios";
import { baseURL } from "@/api";

export async function getReportData(id: string): Promise<ReportData> {
  return (await axios.get<ReportData>(baseURL + "/reports/" + id)).data;
}
