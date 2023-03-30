<template>
    <div id="map"></div>
</template>
  
<script setup lang="ts">
import { getXMLinfo } from "@/components/common/map/api";
import { onMounted } from 'vue'
import { baseURL } from "@/api";

import "leaflet/dist/leaflet.css";
import L from "leaflet";

const props = defineProps<{ id: string }>();
const xmlImageInfoDoc: Document = await getXMLinfo(props.id);

onMounted(() => {
    // Base layers
    //  .. OpenStreetMap
    let osm: L.Layer = L.tileLayer("https://{s}.tile.osm.org/{z}/{x}/{y}.png", {attribution: "&copy; <a href='http://osm.org/copyright'>OpenStreetMap</a> contributors"});

    // Overlay layers (TMS)
    ////////
    let lyr: L.Layer = L.tileLayer(baseURL + "/images/tile/" + props.id + "/{z}/{x}/{y}", {tms: true, opacity: 1, attribution: ""});
    ////////

    // Map
    let map: L.Map = L.map('map', {
        center: [
            parseFloat(xmlImageInfoDoc.getElementsByTagName("Origin")[0].attributes[0].nodeValue as string),  // x
            parseFloat(xmlImageInfoDoc.getElementsByTagName("Origin")[0].attributes[1].nodeValue as string)  // y
        ],
        zoom: parseInt(xmlImageInfoDoc.getElementsByTagName("TileSet")[0].attributes[0].nodeValue as string),
        minZoom: parseInt(xmlImageInfoDoc.getElementsByTagName("TileSet")[0].attributes[0].nodeValue as string),
        maxZoom: parseInt(xmlImageInfoDoc.getElementsByTagName("TileSet")[xmlImageInfoDoc.getElementsByTagName("TileSet").length - 1].attributes[0].nodeValue as string),
        layers: [osm]
    });

    let basemaps = {"OpenStreetMap": osm}
    let overlaymaps = {"Layer": lyr}


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
})

</script>
  
<style scoped lang="scss">
#map {
    width: 90%;
    height: 600px;
    overflow: hidden;
}
</style>
  