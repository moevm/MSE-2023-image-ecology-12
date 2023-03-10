<template>
  <div class="container-lg mt-3">
    <h3>Очередь обработки</h3>
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
import { MapInfo } from "@/types/maps";
import { getQueueInfo } from "@/components/routes/queue/api";

const columnDefs: ColDef<MapInfo>[] = [
  { headerName: "Id", field: "id", flex: 2, rowDrag: true },
  { headerName: "Дата загрузки", field: "uploadDate", flex: 5 },
  { headerName: "Прогресс", field: "progress", flex: 6 },
  { headerName: "Статус", field: "status", flex: 7 },
];

const options: GridOptions<MapInfo> = {
  ...getDefaultGridOptions(),
  domLayout: "autoHeight",
  rowDragManaged: true,
  animateRows: true,
};

const data = await getQueueInfo();
</script>

<style scoped lang="scss"></style>
