import { MapInfo } from "@/types/maps";

export function getMapsInfo(): Promise<MapInfo[]> {
  return Promise.resolve([
    {
      id: 1,
      date: "2023-03-01T12:10:09",
      size: 100,
      ready: false,
      name: "Лес 1",
    },
    {
      id: 2,
      date: "2023-03-02T13:10:09",
      size: 200,
      ready: false,
      name: "Лес 2",
    },
    {
      id: 3,
      date: "2023-03-03T14:10:09",
      size: 300,
      ready: true,
      name: "Лес 3",
    },
    {
      id: 4,
      date: "2023-03-04T15:10:09",
      size: 100,
      ready: false,
      name: "Лес 4",
    },
    {
      id: 5,
      date: "2023-03-08T13:10:09",
      size: 200,
      ready: true,
      name: "Лес 5",
    },
    {
      id: 6,
      date: "2023-03-07T17:10:09",
      size: 100,
      ready: false,
      name: "Лес 6",
    },
    {
      id: 7,
      date: "2023-03-06T12:10:09",
      size: 200,
      ready: true,
      name: "Лес 7",
    },
    {
      id: 8,
      date: "2023-03-05T19:10:09",
      size: 400,
      ready: false,
      name: "Лес 8",
    },
  ]);
}
