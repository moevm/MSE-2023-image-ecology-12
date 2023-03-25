import { ReportData } from "@/types/reports";

export function getReportData(id: string): Promise<ReportData> {
  return Promise.resolve({
    mapId: id,
    anomalies: [
      { id: "1", name: "Лес", coordinates: [10, 10], area: 100 },
      {
        id: "2",
        name: "Полянка",
        coordinates: [20, 15],
        area: 200,
      },
      {
        id: "4",
        name: "Вырубка",
        coordinates: [5, 5],
        area: 300,
      },
      {
        id: "3",
        name: "Пожар",
        coordinates: [5, 5],
        area: 50,
      },
      {
        id: "5",
        name: "Пожар",
        coordinates: [6, 6],
        area: 50,
      },
    ],
  });
}
