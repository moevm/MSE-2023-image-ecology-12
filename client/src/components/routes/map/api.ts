import { Report } from "@/types/reports";

export function getReport(id: number): Promise<Report> {
  return Promise.resolve({
    id,
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
  });
}
