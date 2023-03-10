import { createApp } from "vue";
import { router } from "@/router";
import App from "@/App.vue";
import "bootstrap";
import "bootstrap-icons/font/bootstrap-icons.css";
import "ag-grid-community/styles/ag-grid.css";
import "ag-grid-community/styles/ag-theme-alpine.css";

createApp(App).use(router).mount("#app");
