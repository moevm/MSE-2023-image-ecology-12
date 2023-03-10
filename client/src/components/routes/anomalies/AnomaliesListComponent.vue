<template>
  <div class="container-lg mt-3">
    <h3>База аномалий</h3>
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
import { AnomalyInfo } from "@/types/anomalies";
import { getAnomaliesInfo } from "@/components/routes/anomalies/api";

const columnDefs: ColDef<AnomalyInfo>[] = [
  { headerName: "Id", field: "id", flex: 2, rowDrag: true },
  { headerName: "Название", field: "name", flex: 4 },
  { headerName: "Площадь", field: "area", flex: 4 },
  { headerName: "Дата загрузки", field: "uploadDate", flex: 5 },
  { headerName: "Дата обнаружения", field: "detectDate", flex: 5 },
];

const options: GridOptions<AnomalyInfo> = {
  ...getDefaultGridOptions(),
  domLayout: "autoHeight",
};

const data = await getAnomaliesInfo();
</script>

<style scoped lang="scss"></style>
