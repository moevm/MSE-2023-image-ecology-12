<template>
  <div class="container-lg mt-3">
    <h3>Загруженные карты</h3>
    <AgGridVue
      class="ag-theme-alpine"
      :column-defs="columnDefs"
      :row-data="data"
      :grid-options="options"
    />
  </div>
</template>

<script setup lang="ts">
import { AgGridVue } from "ag-grid-vue3";
import { ColDef, GridOptions } from "ag-grid-community";
import { getDefaultGridOptions } from "@/ag-grid/factory";
import { getMapsInfo } from "@/components/routes/maps/api";
import { MapInfo } from "@/types/maps";

const columnDefs: ColDef<MapInfo>[] = [
  { headerName: "Id", field: "id", flex: 2 },
  { headerName: "Дата загрузки", field: "date", flex: 5 },
  { headerName: "Размер", field: "size", flex: 6 },
  { headerName: "Обработано", field: "ready", flex: 7 },
];

const options: GridOptions<MapInfo> = {
  ...getDefaultGridOptions(),
  domLayout: "autoHeight",
};

const data = await getMapsInfo();
</script>

<style scoped lang="scss"></style>
