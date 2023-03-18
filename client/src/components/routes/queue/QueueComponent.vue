<template>
  <div class="container-lg mt-3">
    <h3>Очередь обработки</h3>
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
import { getQueueInfo } from "@/components/routes/queue/api";
import { QueueItemInfo } from "@/types/queue";
import { dateFormatter } from "@/ag-grid/formatters";
import { routeNames } from "@/router";
import { useRouter } from "vue-router";
import { QueueStatus } from "@/config/queue";
import StatusRenderer from "@/components/routes/queue/components/StatusRenderer.vue";

const router = useRouter();

const columnDefs: ColDef<QueueItemInfo>[] = [
  { headerName: "Id", field: "id", flex: 2, rowDrag: true },
  { headerName: "Название", field: "name", flex: 3 },
  {
    headerName: "Дата загрузки",
    field: "uploadDate",
    flex: 5,
    valueFormatter: dateFormatter,
  },
  { headerName: "Прогресс", field: "progress", flex: 6 },
  {
    headerName: "Статус",
    field: "status",
    flex: 7,
    cellRenderer: StatusRenderer,
  },
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
        tooltip: "Переместить наверх очереди",
        icon: "bi bi-arrow-up",
        button: "btn-success",
      },
      {
        tooltip: "Переместить вниз очереди",
        icon: "bi bi-arrow-down",
        button: "btn-warning",
      },
      {
        tooltip: "Пауза",
        icon: "bi bi-pause",
        button: "btn-danger",
        hide: (data) => data.status === QueueStatus.stopped,
      },
      {
        hide: (data) => data.status !== QueueStatus.stopped,
        tooltip: "Возобновить",
        icon: "bi bi-play",
        button: "btn-info",
      },
    ]),
  },
];

const options: GridOptions<QueueItemInfo> = {
  ...getDefaultGridOptions(),
  domLayout: "autoHeight",
  rowDragManaged: true,
  animateRows: true,
};

const data = await getQueueInfo();
</script>

<style scoped lang="scss"></style>
