import axios from "axios";
import { baseURL } from "@/api";

export async function getXMLinfo(id: string): Promise<Document> {
  const xmlImageInfo: string = (
    await axios.get<string>(baseURL + "/images/tile_map_resource/" + id)
  ).data;
  const parser: DOMParser = new DOMParser();
  const xmlDoc: Document = parser.parseFromString(xmlImageInfo, "text/xml");
  return xmlDoc;
}

export async function getForestPolygon(id: string): Promise<number[][][]> {
  const forestPolygon: number[][][] = (
    await axios.get<number[][][]>(baseURL + "/images/forest/" + id)
  ).data;
  return forestPolygon;
}
