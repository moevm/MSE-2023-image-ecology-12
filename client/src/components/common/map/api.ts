import axios from "axios";
import "leaflet/dist/leaflet.css";
import L, { LatLngExpression, Polygon } from "leaflet";

import { baseURL } from "@/api";


export async function getXMLinfo(id: string): Promise<Document | undefined> {
  const xmlImageInfo = (
    await axios.get<string | 404>(baseURL + "/images/tile_map_resource/" + id)
  ).data;

  if (xmlImageInfo !== 404) {
    const parser: DOMParser = new DOMParser();
    return parser.parseFromString(xmlImageInfo, "text/xml");
  }
}


export async function getForestPolygon(id: string): Promise<number[][][] | undefined> {
  let response = (await axios.get<number[][][] | 404>(baseURL + "/images/forest/" + id)).data;
  
  if (response !== 404) {
    return response;
  }
}


export function init_map() {
  //  OpenStreetMap.
  let osm: L.Layer = L.tileLayer("https://{s}.tile.osm.org/{z}/{x}/{y}.png", {
    attribution:
      "&copy; <a href='http://osm.org/copyright'>OpenStreetMap</a> contributors",
  });

  // Map.
  let map: L.Map = L.map("map", {
    center: [59.9375, 30.308611],
    zoom: 10,
    minZoom: 5,
    maxZoom: 15,
    layers: [osm],
  });

  let basemaps = { OpenStreetMap: osm };

  // Add base layers
  let controlLayer: L.Control.Layers = L.control.layers(basemaps, undefined, { collapsed: false });
  controlLayer.addTo(map);

  return {"map": map, "controlLayer": controlLayer}
}


export function add_tile_layer_map(map: L.Map, controlLayer: L.Control.Layers, id: string, xmlImageInfoDoc: Document) {
  // Overlay layers (TMS).
  let lyr: L.Layer = L.tileLayer(
    baseURL + "/images/tile/" + id + "/{z}/{x}/{y}",
    { tms: true, opacity: 1, attribution: "" }
  );

  // Add layer to map.
  controlLayer.addOverlay(lyr, "Image");

  // Fit to overlay bounds (SW and NE points with (lat, lon))
  map.fitBounds([
    [
      parseFloat(
        xmlImageInfoDoc.getElementsByTagName("BoundingBox")[0].attributes[1]
          .nodeValue as string
      ), // miny
      parseFloat(
        xmlImageInfoDoc.getElementsByTagName("BoundingBox")[0].attributes[2]
          .nodeValue as string
      ), // maxx
    ],
    [
      parseFloat(
        xmlImageInfoDoc.getElementsByTagName("BoundingBox")[0].attributes[3]
          .nodeValue as string
      ), // maxy
      parseFloat(
        xmlImageInfoDoc.getElementsByTagName("BoundingBox")[0].attributes[0]
          .nodeValue as string
      ), // minx
    ],
  ]);

  // Set zoom according to tile layer parameters.
  map.setZoom(parseInt(
    xmlImageInfoDoc.getElementsByTagName("TileSet")[0].attributes[0]
      .nodeValue as string
  ));

  map.setMinZoom(parseInt(
    xmlImageInfoDoc.getElementsByTagName("TileSet")[0].attributes[0]
      .nodeValue as string
  ));

  map.setMaxZoom(parseInt(
    xmlImageInfoDoc.getElementsByTagName("TileSet")[
      xmlImageInfoDoc.getElementsByTagName("TileSet").length - 1
    ].attributes[0].nodeValue as string
  ));
}


export function add_forest_polygon(map: L.Map, controlLayer: L.Control.Layers, forestPolygonArr: number[][][]) {
  // Forest Polygon Layer.
  let forestPolygon: Polygon = L.polygon(
    forestPolygonArr as LatLngExpression[][],
    { color: "green", fillOpacity: 0.4 }
  );
  let forestPolygonLayer: L.LayerGroup = L.layerGroup([forestPolygon]);

  // Add layer to map.
  controlLayer.addOverlay(forestPolygonLayer, "<span style='color: green'>Forest </span>");

  // Fit to overlay bounds (SW and NE points with (lat, lon))
  map.fitBounds([
    [
      forestPolygonArr[0][0][0], // miny
      forestPolygonArr[0][1][1], // maxx
    ],
    [
      forestPolygonArr[0][1][0], // maxy
      forestPolygonArr[0][0][1], // minx
    ],
  ]);
}
