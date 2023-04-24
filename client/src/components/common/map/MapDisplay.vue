<template>
  <div id="map"></div>
</template>

<script setup lang="ts">
import { getXMLinfo, getForestPolygon, init_map, add_tile_layer_map, add_forest_polygon } from "@/components/common/map/api";
import { onMounted } from "vue";

const props = defineProps<{ id: string }>();
const xmlImageInfoDoc = await getXMLinfo(props.id);
let forestPolygonArr = await getForestPolygon(props.id);

onMounted(() => {
  let mapAndControl = init_map();

  if (forestPolygonArr) {
    add_forest_polygon(
      mapAndControl.map, 
      mapAndControl.controlLayer, 
      forestPolygonArr
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
