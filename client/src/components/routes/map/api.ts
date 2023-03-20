import { Report } from "@/types/reports";
import axios from "axios";
import { baseURL } from "@/api";

export async function getXMLinfo(id: string): Promise<Document> {
  let xmlImageInfo: string = "";
  await axios.get<string>(baseURL + "/images/tile_map_resource/" + id).then((response: any) => {
    xmlImageInfo = response.data;
  });
  let parser: DOMParser = new DOMParser();
  let xmlDoc: Document = parser.parseFromString(xmlImageInfo, "text/xml");
  return xmlDoc;
}

export function getReport(id: string): Promise<Report> {
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
