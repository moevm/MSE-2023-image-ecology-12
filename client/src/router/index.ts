import { createRouter, createWebHistory, RouteRecordRaw } from "vue-router";

export const routeNames = {
  Reports: "Reports",
  Queue: "Queue",
  Map: "Map",
};

export const routePaths = {
  [routeNames.Reports]: "/",
  [routeNames.Queue]: "/queue",
  [routeNames.Map]: "/map/:id",
};

export const routes: RouteRecordRaw[] = [
  {
    name: routeNames.Reports,
    path: routePaths[routeNames.Reports],
    component: () => import("@/views/ReportsView.vue"),
  },
  {
    name: routeNames.Queue,
    path: routePaths[routeNames.Queue],
    component: () => import("@/views/QueueView.vue"),
  },
  {
    name: routeNames.Map,
    path: routePaths[routeNames.Map],
    component: () => import("@/views/MapView.vue"),
  },
];

export const router = createRouter({
  history: createWebHistory(),
  routes,
});
