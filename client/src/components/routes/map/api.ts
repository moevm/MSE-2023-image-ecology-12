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
