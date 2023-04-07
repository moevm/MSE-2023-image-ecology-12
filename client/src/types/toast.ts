export enum ToastTypes {
  primary = "primary",
  secondary = "secondary",
  success = "success",
  info = "info",
  danger = "danger",
  warning = "warning",
  light = "light",
  dark = "dark",
}

export interface ToastData {
  id: number;
  type?: ToastTypes;
  title?: string;
  body?: string;
  time?: number;
}
