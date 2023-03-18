<template>
  <div class="container-lg">
    <h2 class="text-center mt-2 text-primary">Просмотр отчёта №{{ id }}</h2>
    <AgGridVue
      class="ag-theme-alpine mt-3"
      :row-data="reportData.anomalies"
      :column-defs="columnDefs"
      :grid-options="options"
    />
  </div>
</template>

<script setup lang="ts">
import { AgGridVue } from "ag-grid-vue3";
import { getReportData } from "@/components/routes/report/api";
import { ColDef, GridOptions } from "ag-grid-community";
import { AnomalyInfo } from "@/types/anomalies";
import { getActionsColDef, getDefaultGridOptions } from "@/ag-grid/factory";
import { routeNames } from "@/router";
import { useRouter } from "vue-router";

const router = useRouter();

const props = defineProps<{ id: number }>();

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
        tooltip: "Открыть карту",
        icon: "bi bi-map",
        button: "btn-primary",
        onClicked: (action, data) =>
          router.push({
            name: routeNames.Map,
            params: { id: reportData?.mapId },
          }),
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
