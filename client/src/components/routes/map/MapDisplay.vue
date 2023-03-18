<template>
    <div id="map"></div>
</template>
  
<script setup lang="ts">
import { useRoute } from "vue-router";
import { getXMLinfo } from "@/components/routes/map/api";
import ObjectGroupsList from "@/components/common/ObjectGroupsList.vue";

import L from "leaflet";

const route = useRoute();
const id: string = route.params.id;
const xmlImageInfoDoc: Document = await getXMLinfo(id);
const serverURL = import.meta.env.SERVER_URI;


// Base layers
//  .. OpenStreetMap
var osm = L.tileLayer("http://{s}.tile.osm.org/{z}/{x}/{y}.png", {attribution: "&copy; <a href='http://osm.org/copyright'>OpenStreetMap</a> contributors"});

// Overlay layers (TMS)
////////
var lyr = L.tileLayer(serverURL + id + "/{z}/{x}/{y}.png", {tms: true, opacity: 0.7, attribution: ""});
////////

// Map
var map = L.map('map', {
    center: [
        parseFloat(xmlImageInfoDoc.getElementsByTagName("Origin")[0].attributes[0].nodeValue as string),  // x
        parseFloat(xmlImageInfoDoc.getElementsByTagName("Origin")[0].attributes[1].nodeValue as string)  // y
    ],
    zoom: parseInt(xmlImageInfoDoc.getElementsByTagName("TileSet")[0].attributes[0].nodeValue as string),
    minZoom: parseInt(xmlImageInfoDoc.getElementsByTagName("TileSet")[xmlImageInfoDoc.getElementsByTagName("TileSet").length - 1].attributes[0].nodeValue as string),
    maxZoom: parseInt(xmlImageInfoDoc.getElementsByTagName("TileSet")[0].attributes[0].nodeValue as string),
    layers: [osm]
});

var basemaps = {"OpenStreetMap": osm}
var overlaymaps = {"Layer": lyr}


// Add base layers
L.control.layers(basemaps, overlaymaps, {collapsed: false}).addTo(map);

// Fit to overlay bounds (SW and NE points with (lat, lon))
map.fitBounds([
    [
        parseFloat(xmlImageInfoDoc.getElementsByTagName("BoundingBox")[0].attributes[1].nodeValue as string), // miny
        parseFloat(xmlImageInfoDoc.getElementsByTagName("BoundingBox")[0].attributes[2].nodeValue as string)  // maxx
    ], 
    [
        parseFloat(xmlImageInfoDoc.getElementsByTagName("BoundingBox")[0].attributes[3].nodeValue as string),  // maxy
        parseFloat(xmlImageInfoDoc.getElementsByTagName("BoundingBox")[0].attributes[0].nodeValue as string)  // minx
    ] 
]);
</script>
  
<style scoped lang="scss"></style>
  