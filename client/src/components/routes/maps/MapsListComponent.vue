<template>
  <div class="container-lg mt-3">
    <h3>Загруженные карты</h3>
    <AgGridVue
      class="ag-theme-alpine"
      :column-defs="columnDefs"
      :row-data="data"
      :grid-options="options"
      @grid-ready="fitActionsColumn"
    />
  </div>
</template>

<script setup lang="ts">
import { AgGridVue } from "ag-grid-vue3";
import { ColDef, GridOptions } from "ag-grid-community";
import {
  fitActionsColumn,
  getActionsColDef,
  getDefaultGridOptions,
} from "@/ag-grid/factory";
import { getMapsInfo } from "@/components/routes/maps/api";
import { MapInfo } from "@/types/maps";
import { dateFormatter } from "@/ag-grid/formatters";
import { useRouter } from "vue-router";
import { routeNames } from "@/router";

const router = useRouter();

const columnDefs: ColDef<MapInfo>[] = [
  { headerName: "Id", field: "id", flex: 2, minWidth: 80 },
  {
    headerName: "Дата загрузки",
    field: "date",
    flex: 5,
    minWidth: 180,
    valueFormatter: dateFormatter,
  },
  { headerName: "Размер", field: "size", flex: 5, minWidth: 180 },
  { headerName: "Обработано", field: "ready", flex: 3, minWidth: 200 },
  {
    ...getActionsColDef([
      {
        tooltip: "Открыть карту",
        icon: "bi bi-map",
        button: "btn-secondary",
        onClicked: (action, data) =>
          router.push({ name: routeNames.Map, params: { id: data.id } }),
      },
      {
        tooltip: "Открыть отчёт",
        icon: "bi bi-file-text",
        button: "btn-primary",
        hide: (data) => !data.ready,
      },
    ]),
  },
];

const options: GridOptions<MapInfo> = {
  ...getDefaultGridOptions(),
  domLayout: "autoHeight",
};

const data = await getMapsInfo();
</script>

<style scoped lang="scss"></style>
