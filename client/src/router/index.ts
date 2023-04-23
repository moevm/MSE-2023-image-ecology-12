import { createRouter, createWebHistory, RouteRecordRaw } from "vue-router";

export const routeNames = {
  MapsList: "Maps",
  Queue: "Queue",
  ReportsList: "Reports",
  AnomaliesList: "Anomalies",
  Upload: "Upload",
  Map: "Map",
  Report: "Report",
  Anomaly: "Anomaly",
};

export const routePaths = {
  [routeNames.MapsList]: "/",
  [routeNames.Queue]: "/queue",
  [routeNames.ReportsList]: "/reports",
  [routeNames.AnomaliesList]: "/anomalies",
  [routeNames.Upload]: "/upload",
  [routeNames.Map]: "/map/:id",
  [routeNames.Report]: "/report/:id",
  [routeNames.Anomaly]: "/anomaly/:id",
};

export const routes: RouteRecordRaw[] = [
  {
    name: routeNames.MapsList,
    path: routePaths[routeNames.MapsList],
    component: () => import("@/views/MapsListView.vue"),
  },
  {
    name: routeNames.Queue,
    path: routePaths[routeNames.Queue],
    component: () => import("@/views/QueueView.vue"),
  },
  {
    name: routeNames.ReportsList,
    path: routePaths[routeNames.ReportsList],
    component: () => import("@/views/ReportsListView.vue"),
  },
  {
    name: routeNames.AnomaliesList,
    path: routePaths[routeNames.AnomaliesList],
    component: () => import("@/views/AnomaliesListView.vue"),
  },
  {
    name: routeNames.Upload,
    path: routePaths[routeNames.Upload],
    component: () => import("@/views/UploadView.vue"),
  },
  {
    name: routeNames.Map,
    path: routePaths[routeNames.Map],
    component: () => import("@/views/MapView.vue"),
    props: (route) => ({ id: route.params.id }),
  },
  {
    name: routeNames.Report,
    path: routePaths[routeNames.Report],
    component: () => import("@/views/ReportView.vue"),
    props: (route) => ({ id: route.params.id }),
  },
  {
    name: routeNames.Anomaly,
    path: routePaths[routeNames.Anomaly],
    component: () => import("@/views/AnomalyView.vue"),
    props: (route) => ({ id: route.params.id }),
  },
];

export const router = createRouter({
  history: createWebHistory(),
  routes,
});
