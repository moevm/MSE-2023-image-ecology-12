import axios from "axios";
import { baseURL } from "@/api";

export async function getXMLinfo(id: string): Promise<Document> {
  let xmlImageInfo: string = (await axios.get<string>(baseURL + "/images/tile_map_resource/" + id)).data;
  let parser: DOMParser = new DOMParser();
  let xmlDoc: Document = parser.parseFromString(xmlImageInfo, "text/xml");
  return xmlDoc;
}

export async function getForestPolygon(id: string): Promise<number[][][]> {
  let forestPolygon: number[][][] = (await axios.get<number[][][]>(baseURL + "/images/forest/" + id)).data;
  return forestPolygon;
}