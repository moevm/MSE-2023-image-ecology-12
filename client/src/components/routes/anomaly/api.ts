import { AnomalyData } from "@/types/anomalies";

export function getAnomalyData(id: number): Promise<AnomalyData> {
  return Promise.resolve({
    reportId: id,
    mapId: id,
    area: 100,
    name: `Аномалия ${id}`,
    coordinates: [10, 10],
  });
}
