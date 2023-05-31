<template>
  <div id="map"></div>
</template>

<script setup lang="ts">
import {
  getXMLinfo,
  getAnomalies,
  initMap,
  addTileLayerMap,
  addAnomalies
} from "@/components/common/map/api";
import { onMounted, ref } from "vue";
import L  from "leaflet";
import "leaflet/dist/leaflet.css";
import iconRetinaUrl from 'leaflet/dist/images/marker-icon-2x.png';
import iconUrl from 'leaflet/dist/images/marker-icon.png';
import shadowUrl from 'leaflet/dist/images/marker-shadow.png';


let addMarker = ref<(markerPosition: [number, number]) => L.Marker>();
let removeMarker = ref<(marker: L.Marker) => void>();
let flyToCoordinates = ref<(coordinates: [number, number]) => void>();
defineExpose({addMarker, removeMarker, flyToCoordinates});

const props = defineProps<{ id: string}>();
const xmlImageInfoDoc = await getXMLinfo(props.id);
let anomaliesList = await getAnomalies(props.id);

onMounted(() => {
  // Загружаем картинки и параметры маркера в leaflet 
  L.Marker.prototype.options.icon = L.icon({
    iconRetinaUrl: iconRetinaUrl,
    iconUrl: iconUrl,
    shadowUrl: shadowUrl,
    iconSize: [25, 41],
    iconAnchor: [12, 41],
    popupAnchor: [1, -34],
    tooltipAnchor: [16, -28],
    shadowSize: [41, 41],
  });

  let mapAndControl = initMap();
  if (anomaliesList) {
    addAnomalies(
      mapAndControl.map, 
      mapAndControl.controlLayer, 
      anomaliesList
    );
  }

  if (xmlImageInfoDoc) {
    addTileLayerMap(
      mapAndControl.map, 
      mapAndControl.controlLayer, 
      props.id, 
      xmlImageInfoDoc
    );
  }

  // Создаем насколько функций для использования родительскими элементами для управления картой.
  addMarker.value = (markerPosition: [number, number]) => {
    let marker = new L.Marker(markerPosition);
    marker.addTo(mapAndControl.map);
    
    return marker;
  }

  flyToCoordinates.value = (coordinates: [number, number]) => {
    mapAndControl.map.panTo(coordinates);
  }

  removeMarker.value = (marker: L.Marker) => {
    mapAndControl.map.removeLayer(marker);
  }
});
</script>

<style scoped lang="scss">
#map {
  width: 90%;
  height: 600px;
  overflow: hidden;
}
</style>
