import { Report, ReportInfo } from "@/types/reports";

export function getReportsInfo(): Promise<ReportInfo[]> {
  return Promise.resolve([
    { id: 1, date: "2023-03-01T12:01:10" },
    { id: 2, date: "2023-03-01T12:01:10" },
    { id: 3, date: "2023-03-01T12:01:10" },
    { id: 4, date: "2023-03-01T12:01:10" },
    { id: 5, date: "2023-03-01T12:01:10" },
  ]);
}

export function getReportsList(): Promise<Report[]> {
  return Promise.resolve(
    [1, 2, 3, 4, 5, 6].map((i) => ({
      id: i,
      groups: [
        {
          name: "Найденные объекты",
          objects: [
            { name: "Лес", coordinates: [10, 10] },
            { name: "Полянка", coordinates: [20, 15] },
          ],
        },
        {
          name: "Найденные Аномалии",
          objects: [
            { name: "Вырубка", coordinates: [5, 5] },
            { name: "Пожар", coordinates: [5, 5] },
          ],
        },
      ],
    }))
  );
}
