<template>
  <div id="map"></div>
</template>

<script setup lang="ts">
import {
  getXMLinfo,
  getAnomalies,
  init_map,
  add_tile_layer_map,
  add_anomalies
} from "@/components/common/map/api";
import { onMounted } from "vue";

const props = defineProps<{ id: string }>();
const xmlImageInfoDoc = await getXMLinfo(props.id);
let anomaliesList = await getAnomalies(props.id);

onMounted(() => {
  let mapAndControl = init_map();

  if (anomaliesList) {
    add_anomalies(
      mapAndControl.map, 
      mapAndControl.controlLayer, 
      anomaliesList
    );
  }

  if (xmlImageInfoDoc) {
    add_tile_layer_map(
      mapAndControl.map, 
      mapAndControl.controlLayer, 
      props.id, 
      xmlImageInfoDoc
    );
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
