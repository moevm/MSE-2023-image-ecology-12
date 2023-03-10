import { MapInfo } from "@/types/maps";

export function getMapsInfo(): Promise<MapInfo[]> {
  return Promise.resolve([
    { id: 1, date: "2023-03-01T12:10:09", size: 100, ready: false },
    { id: 2, date: "2023-03-02T13:10:09", size: 200, ready: false },
    { id: 3, date: "2023-03-03T14:10:09", size: 300, ready: true },
    { id: 4, date: "2023-03-04T15:10:09", size: 100, ready: false },
    { id: 5, date: "2023-03-08T13:10:09", size: 200, ready: true },
    { id: 6, date: "2023-03-07T17:10:09", size: 100, ready: false },
    { id: 7, date: "2023-03-06T12:10:09", size: 200, ready: true },
    { id: 8, date: "2023-03-05T19:10:09", size: 400, ready: false },
  ]);
}
