import { ColDef, GridOptions } from "ag-grid-community";
import { agGridLocalization } from "@/ag-grid/localization";

export function getDefaultColDef(): ColDef {
  return {
    filter: true,
    sortable: true,
    editable: false,
    resizable: true,
  };
}

export function getDefaultGridOptions(): GridOptions {
  return {
    defaultColDef: getDefaultColDef(),
    localeText: agGridLocalization,
    suppressMenuHide: true,
    enableCellTextSelection: true,
    suppressDragLeaveHidesColumns: true,
  };
}
