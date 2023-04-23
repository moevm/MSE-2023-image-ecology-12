<template>
  <div class="container-lg">
    <h2 class="text-center mt-2 text-primary">Просмотр аномалии №{{ id }}</h2>
    <div class="row justify-content-end">
      <router-link
        class="col-auto"
        :to="{ name: routeNames.Map, params: { id: anomalyData?.mapId } }"
      >
        <button class="btn btn-secondary">Открыть карту</button>
      </router-link>
      <router-link
        class="col-auto"
        :to="{ name: routeNames.Report, params: { id: anomalyData?.reportId } }"
      >
        <button class="btn btn-primary">Открыть отчёт</button>
      </router-link>
    </div>

    <AgGridVue
      class="ag-theme-alpine mt-3"
      :column-defs="columnDefs"
      :grid-options="options"
      :row-data="[anomalyData]"
      style="height: 93px"
      @grid-ready="fitActionsColumn"
    />
  </div>
</template>

<script setup lang="ts">
import { ColDef, GridOptions } from "ag-grid-community";
import { AnomalyInfo } from "@/types/anomalies";
import { dateFormatter } from "@/ag-grid/formatters";
import {
  fitActionsColumn,
  getActionsColDef,
  getDefaultGridOptions,
} from "@/ag-grid/factory";
import { routeNames } from "@/router";
import { getAnomalyData } from "@/components/routes/anomaly/api";
import { AgGridVue } from "ag-grid-vue3";

const props = defineProps<{ id: string }>();

const columnDefs: ColDef<AnomalyInfo>[] = [
  { headerName: "Название", field: "name", flex: 4, minWidth: 180 },
  { headerName: "Площадь", field: "area", flex: 4, minWidth: 180 },
  {
    headerName: "Дата загрузки",
    field: "uploadDate",
    flex: 5,
    minWidth: 200,
    valueFormatter: dateFormatter,
  },
  {
    headerName: "Дата обнаружения",
    field: "detectDate",
    flex: 5,
    minWidth: 200,
    valueFormatter: dateFormatter,
  },
  {
    ...getActionsColDef([
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
};

const anomalyData = await getAnomalyData(props.id);
</script>

<style scoped lang="scss"></style>
