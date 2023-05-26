import axios, { AxiosError } from "axios";
import "leaflet/dist/leaflet.css";
import L, { LatLngExpression, Polygon } from "leaflet";

import { baseURL } from "@/api";
import { AnomaliesMapData } from "@/types/anomalies";


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


export async function getAnomalies(id: string): Promise<AnomaliesMapData[] | void> {
  return axios.get<AnomaliesMapData[]>(baseURL + "/images/anomalies/" + id).then(response => {
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


export function add_anomalies(map: L.Map, controlLayer: L.Control.Layers, anomaliesList: AnomaliesMapData[]) {
  for (let i = 0; i < anomaliesList.length; i++) {
    window.console.log('Anomaly: ' + anomaliesList[i].color)
    window.console.log('Anomaly: ' + anomaliesList[i].name)
    window.console.log('Anomaly: ' + anomaliesList[i].polygons)
    // Anomaly Polygon Layer.
    let anomalyPolygon: Polygon = L.polygon(
      anomaliesList[i].polygons as LatLngExpression[][],
      { color: anomaliesList[i].color, fillOpacity: 0.4 }
    );
    let anomalyPolygonLayer: L.LayerGroup = L.layerGroup([anomalyPolygon]);

    // Add layer to map.
    controlLayer.addOverlay(
      anomalyPolygonLayer, 
      "<span style='color: " + anomaliesList[i].color + "'> " + anomaliesList[i].name + " </span>"
    );

    // Fit to overlay bounds (SW and NE points with (lat, lon))
    map.fitBounds([
      [
        anomaliesList[i].polygons[0][0][0], // miny
        anomaliesList[i].polygons[0][1][1], // maxx
      ],
      [
        anomaliesList[i].polygons[0][1][0], // maxy
        anomaliesList[i].polygons[0][0][1], // minx
      ],
    ]); 
  }
}
