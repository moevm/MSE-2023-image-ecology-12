import { MapInfo } from "@/types/maps";

export function getMapsInfo(): Promise<MapInfo[]> {
  return Promise.resolve([
    { id: 1, date: "2023-03-01", size: 100, ready: false },
    { id: 2, date: "2023-03-02", size: 200, ready: false },
    { id: 3, date: "2023-03-03", size: 300, ready: true },
    { id: 4, date: "2023-03-04", size: 100, ready: false },
    { id: 5, date: "2023-03-08", size: 200, ready: true },
    { id: 6, date: "2023-03-07", size: 100, ready: false },
    { id: 7, date: "2023-03-06", size: 200, ready: true },
    { id: 8, date: "2023-03-05", size: 400, ready: false },
  ]);
}
