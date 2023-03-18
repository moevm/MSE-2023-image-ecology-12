import { MapAnomaly } from "@/types/maps";

export function getMapData(id: number): Promise<MapAnomaly[]> {
  return Promise.resolve([
    { id: 1, name: "Лес", coordinates: [10, 10], area: 100 },
    { id: 2, name: "Полянка", coordinates: [20, 15], area: 200 },
    { id: 4, name: "Вырубка", coordinates: [5, 5], area: 300 },
    { id: 3, name: "Пожар", coordinates: [5, 5], area: 50 },
    { id: 5, name: "Пожар", coordinates: [6, 6], area: 50 },
  ]);
}
