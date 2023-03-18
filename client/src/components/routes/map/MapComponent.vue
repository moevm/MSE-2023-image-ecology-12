<template>
  <div class="container-lg">
    <h2 class="text-center mt-2 text-primary">Просмотр карты №{{ id }}</h2>
    <AgGridVue
      class="ag-theme-alpine mt-3"
      :row-data="mapData"
      :column-defs="columnDefs"
      :grid-options="options"
      @grid-ready="fitActionsColumn"
    />
    <div class="d-flex justify-content-center mt-3">
      <img src="/src/assets/img.png" />
    </div>
  </div>
</template>

<script setup lang="ts">
import { getMapData } from "@/components/routes/map/api";
import { AgGridVue } from "ag-grid-vue3";
import { ColDef, GridOptions } from "ag-grid-community";
import { AnomalyInfo } from "@/types/anomalies";
import {
  fitActionsColumn,
  getActionsColDef,
  getDefaultGridOptions,
} from "@/ag-grid/factory";
import { routeNames } from "@/router";
import { useRouter } from "vue-router";

const router = useRouter();

const columnDefs: ColDef<AnomalyInfo>[] = [
  { headerName: "Id", field: "id", flex: 2 },
  { headerName: "Название", field: "name", flex: 4 },
  { headerName: "Площадь", field: "area", flex: 4 },
  {
    ...getActionsColDef([
      {
        tooltip: "Открыть аномалию",
        icon: "bi bi-radioactive",
        button: "btn-danger",
        onClicked: (action, data) =>
          router.push({ name: routeNames.Anomaly, params: { id: data.id } }),
      },
      {
        tooltip: "Показать на карте",
        icon: "bi bi-eye",
        button: "btn-info",
      },
      {
        tooltip: "Открыть отчёт",
        icon: "bi bi-file-text",
        button: "btn-secondary",
        onClicked: (action, data) =>
          router.push({
            name: routeNames.Report,
            params: { id: mapData?.reportId },
          }),
      },
    ]),
  },
];

const options: GridOptions<AnomalyInfo> = {
  ...getDefaultGridOptions(),
  pagination: true,
  paginationPageSize: 4,
  domLayout: "autoHeight",
};

const props = defineProps<{ id: number }>();
const mapData = await getMapData(props.id);
</script>

<style scoped lang="scss"></style>
