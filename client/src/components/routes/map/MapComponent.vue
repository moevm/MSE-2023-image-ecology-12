<template>
  <div class="container-lg">
    <h2 class="text-center mt-2 text-primary">Просмотр карты №{{ id }}</h2>
    <div v-if="mapData" class="row justify-content-between">
      <h3 class="col">Аномалии</h3>
      <router-link
        class="col-auto"
        :to="{ name: routeNames.Report, params: { id: mapData?.reportId } }"
      >
        <button class="btn btn-primary">Открыть отчёт</button>
      </router-link>
    </div>
    <AgGridVue
      v-if="mapData"
      class="ag-theme-alpine mt-3"
      :row-data="mapData.anomalies"
      :column-defs="columnDefs"
      :grid-options="options"
      @grid-ready="fitActionsColumn"
    />
    <div class="d-flex justify-content-center mt-3">
      <MapDisplay :id="id" />
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

import MapDisplay from "@/components/common/map/MapDisplay.vue";

const router = useRouter();
const props = defineProps<{ id: string }>();

const columnDefs: ColDef<AnomalyInfo>[] = [
  { headerName: "Id", field: "id", flex: 2, minWidth: 120 },
  { headerName: "Название", field: "name", flex: 4, minWidth: 180 },
  { headerName: "Площадь", field: "area", flex: 4, minWidth: 180 },
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
    ]),
  },
];

const options: GridOptions<AnomalyInfo> = {
  ...getDefaultGridOptions(),
  pagination: true,
  paginationPageSize: 4,
  domLayout: "autoHeight",
};

const mapData = await getMapData(props.id);
</script>

<style scoped lang="scss"></style>
