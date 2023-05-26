import { AnomalyInfo } from "@/types/anomalies";
import axios from "axios";
import { baseURL } from "@/api";

export async function getAnomaliesInfo(): Promise<AnomalyInfo[]> {
  return (await axios.get<AnomalyInfo[]>(baseURL + "/anomalies/")).data;
}
