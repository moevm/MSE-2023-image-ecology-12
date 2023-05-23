import { AnomalyInfo } from "@/types/anomalies";
import axios from "axios";
import { baseURL } from "@/api";

export async function getAnomaliesInfo(): Promise<AnomalyInfo[]> {
  return (await axios.get<AnomalyInfo[]>(baseURL + "/anomalies/")).data;
}

/*
export function getAnomaliesInfo(): Promise<AnomalyInfo[]> {
  return Promise.resolve([
    {
      id: "1",
      area: 123,
      name: "Заросшая просека",
      uploadDate: "2023-03-01T13:03:03",
      detectDate: "2023-03-02T12:03:03",
    },
    {
      id: "2",
      area: 143,
      name: "Вырубка",
      uploadDate: "2023-03-02T13:03:03",
      detectDate: "2023-03-02T16:03:03",
    },
    {
      id: "3",
      area: 421,
      name: "Заросшая просека",
      uploadDate: "2023-03-03T13:03:03",
      detectDate: "2023-03-04T13:03:03",
    },
    {
      id: "4",
      area: 6666,
      name: "Испытания ядерного оружия",
      uploadDate: "2023-03-04T11:03:03",
      detectDate: "2023-03-04T13:03:03",
    },
    {
      id: "5",
      area: 987,
      name: "Падение метеорита",
      uploadDate: "2023-03-05T09:03:03",
      detectDate: "2023-03-06T16:03:03",
    },
  ]);
}*/
