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
import { dateFormatter } from "@/ag-grid/formatters";
import ActionsRenderer from "@/components/renderers/ActionsRenderer.vue";
import { Action } from "@/types/ag-grid/actions";
import { useRouter } from "vue-router";
import { routeNames } from "@/router";

const router = useRouter();

const columnDefs: ColDef<MapInfo>[] = [
  { headerName: "Id", field: "id", flex: 2 },
  {
    headerName: "Дата загрузки",
    field: "date",
    flex: 5,
    valueFormatter: dateFormatter,
  },
  { headerName: "Размер", field: "size", flex: 6 },
  { headerName: "Обработано", field: "ready", flex: 7 },
  {
    headerName: "Действия",
    cellRenderer: ActionsRenderer,
    cellRendererParams: {
      actions: [
        {
          tooltip: "Открыть карту",
          icon: "bi bi-map",
          onClicked: (action, data) =>
            router.push({ name: routeNames.Map, params: { id: data.id } }),
        },
        {
          tooltip: "Открыть отчёт",
          icon: "bi bi-file-text",
          onClicked: (action, data) =>
            router.push({
              /* name: reports */
            }),
          hide: (data) => !data.ready,
        },
      ] as Action<MapInfo>[],
    },
  },
];

const options: GridOptions<MapInfo> = {
  ...getDefaultGridOptions(),
  domLayout: "autoHeight",
};

const data = await getMapsInfo();
</script>

<style scoped lang="scss"></style>
