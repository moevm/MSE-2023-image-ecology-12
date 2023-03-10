<template>
  <div class="container-lg mt-3">
    <h3>Отчёты обработанных карт</h3>
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
import { getReportsInfo } from "@/components/routes/reports/api";
import { ReportInfo } from "@/types/reports";

const columnDefs: ColDef<ReportInfo>[] = [
  { headerName: "Id", field: "id", flex: 2, rowDrag: true },
  { headerName: "Дата загрузки", field: "date", flex: 5 },
];

const options: GridOptions<ReportInfo> = {
  ...getDefaultGridOptions(),
  domLayout: "autoHeight",
};

const data = await getReportsInfo();
</script>

<style scoped lang="scss"></style>
