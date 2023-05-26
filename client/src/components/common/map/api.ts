import axios, { AxiosError } from "axios";
import "leaflet/dist/leaflet.css";
import L, { LatLngExpression, Polygon } from "leaflet";

import { baseURL } from "@/api";


export async function getXMLinfo(id: string): Promise<Document | void> {
  return axios.get<string>(baseURL + "/images/tile_map_resource/" + id).then(response => {
    const parser: DOMParser = new DOMParser();
    return parser.parseFromString(response.data, "text/xml");
  }).catch((err: AxiosError) => {
    if (!err.response || (err.response && err.response.status !== 404)) {
      throw err;
    }
  });
}


export async function getForestPolygon(id: string): Promise<number[][][] | void> {
  return axios.get<number[][][]>(baseURL + "/images/forest/" + id).then(response => {
    return response.data;
  }).catch((err: AxiosError) => {
    if (!err.response || (err.response && err.response.status !== 404)) {
      throw err;
    }
  });
}


export async function getDeforestationPolygon(id: string): Promise<number[][][] | void> {
  return axios.get<number[][][]>(baseURL + "/images/deforestation/" + id).then(response => {
    return response.data;
  }).catch((err: AxiosError) => {
    if (!err.response || (err.response && err.response.status !== 404)) {
      throw err;
    }
  });
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


export function add_deforestation_polygon(map: L.Map, controlLayer: L.Control.Layers, deforestationPolygonArr: number[][][]) {
  // Forest Polygon Layer.
  let deforestationPolygon: Polygon = L.polygon(
      deforestationPolygonArr as LatLngExpression[][],
      { color: "red", fillOpacity: 0.4 }
  );
  let deforestationPolygonLayer: L.LayerGroup = L.layerGroup([deforestationPolygon]);

  // Add layer to map.
  controlLayer.addOverlay(deforestationPolygonLayer, "<span style='color: red'>Deforestation </span>");

  // Fit to overlay bounds (SW and NE points with (lat, lon))
  map.fitBounds([
    [
      deforestationPolygonArr[0][0][0], // miny
      deforestationPolygonArr[0][1][1], // maxx
    ],
    [
      deforestationPolygonArr[0][1][0], // maxy
      deforestationPolygonArr[0][0][1], // minx
    ],
  ]);
}
