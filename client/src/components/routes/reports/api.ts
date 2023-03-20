import { Report } from "@/types/reports";

export function getReportsList(): Promise<Report[]> {
  return Promise.resolve(
    [1, 2, 3, 4, 5, 6].map((i) => ({
      id: "64175d4f530dc2f65cf7c3cc",
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
