<template>
  <div class="container-lg">
    <h2 class="text-center mt-2 text-primary">Просмотр отчёта №{{ id }}</h2>
    <div class="row justify-content-between">
      <h3 class="col">Аномалии</h3>
      <router-link
        class="col-auto"
        :to="{ name: routeNames.Map, params: { id: reportData.mapId } }"
      >
        <button class="btn btn-secondary">Открыть карту</button>
      </router-link>
    </div>
    <AgGridVue
      class="ag-theme-alpine mt-3"
      :row-data="reportData.anomalies"
      :column-defs="columnDefs"
      :grid-options="options"
      @grid-ready="fitActionsColumn"
    />
  </div>
</template>

<script setup lang="ts">
import { AgGridVue } from "ag-grid-vue3";
import { getReportData } from "@/components/routes/report/api";
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

const props = defineProps<{ id: number }>();

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
  domLayout: "autoHeight",
};

const reportData = await getReportData(props.id);
</script>

<style scoped lang="scss"></style>
