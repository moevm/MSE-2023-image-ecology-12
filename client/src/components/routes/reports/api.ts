import { Report } from "@/types/reports";
import axios from "axios";
import { baseURL } from "@/api";


export async function getReportsList(): Promise<Report[]> {
  let db_ids: string[] = [];
  await axios.get<string[]>(baseURL + "/images/").then((response: any) => {
    db_ids = response.data;
  });

  return Promise.resolve(
      db_ids.map((i) => ({
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
