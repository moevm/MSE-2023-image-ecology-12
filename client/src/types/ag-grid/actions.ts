import { ICellRendererParams } from "ag-grid-community";

export interface Action<T = any> {
  tooltip: string;
  icon: string;
  onClicked: <V = any>(
    action: Action<T>,
    params: ICellRendererParams<T, V>
  ) => void;
  hide?: boolean | (<V = any>(data: T, value: V) => boolean);
}
