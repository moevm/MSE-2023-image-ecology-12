import { createApp } from "vue";
import { router } from "@/router";
import App from "@/App.vue";
import "bootstrap";
import "bootstrap-icons/font/bootstrap-icons.css";
import "ag-grid-community/styles/ag-grid.css";
import "ag-grid-community/styles/ag-theme-alpine.css";
import { vBsTooltip } from "@/bootstrap/tooltip";

const app = createApp(App);
app.use(router);
app.directive("bs-tooltip", vBsTooltip);
app.mount("#app");
