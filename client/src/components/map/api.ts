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