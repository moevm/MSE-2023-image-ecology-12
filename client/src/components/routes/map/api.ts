import { MapData } from "@/types/maps";
import { Report } from "@/types/reports";
import axios from "axios";

export async function getXMLinfo(id: string): Promise<Document> {
  const serverURL = import.meta.env.SERVER_URI;
  let xmlImageInfo: string = "";
  await axios.get(serverURL + "/").then((response: string) => {
    xmlImageInfo = response;
  });
  let parser: DOMParser = new DOMParser();
  let xmlDoc: Document = parser.parseFromString(xmlImageInfo, "text/xml");
  return xmlDoc;
}

export function getMapData(id: string): Promise<MapData | null> {
  // Тестовые данные: чётный id - есть аномалии, нечётный -нет
  return Promise.resolve(
    (parseInt(id) % 2).toString()
      ? null
      : {
          reportId: id,
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
        }
  );
}
