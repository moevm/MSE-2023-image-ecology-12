import { AnomalyData } from "@/types/anomalies";

export function getAnomalyData(id: string): Promise<AnomalyData> {
  return Promise.resolve({
    reportId: id,
    mapId: id,
    area: 100,
    name: `Аномалия ${id}`,
    uploadDate: "2023-03-01T13:03:03",
    detectDate: "2023-03-02T12:03:03",
    coordinates: [10, 10],
  });
}
