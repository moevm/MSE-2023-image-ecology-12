<template>
  <nav class="navbar navbar-expand-lg bg-light">
    <div class="container-fluid px-3">
      <a class="navbar-brand" href="#"><i class="bi bi-map fs-2" /></a>
      <button
        class="navbar-toggler"
        type="button"
        data-bs-toggle="collapse"
        data-bs-target="#navbar"
      >
        <span class="navbar-toggler-icon"></span>
      </button>
      <div class="collapse navbar-collapse fs-5 fw-semibold" id="navbar">
        <ul class="navbar-nav me-auto mb-2 mb-lg-0">
          <li v-for="route of routes" :key="route" class="nav-item">
            <router-link
              :to="{ name: route }"
              class="nav-link"
              active-class="active"
            >
              {{ routesTranslation[route] }}
            </router-link>
          </li>
        </ul>
      </div>
    </div>
  </nav>
  <main>
    <router-view />
  </main>
</template>

<script setup lang="ts">
import { routeNames } from "@/router";

const routes = [routeNames.Reports, routeNames.Queue];
const routesTranslation = {
  [routeNames.Reports]: "Отчёты",
  [routeNames.Queue]: "Очередь",
};
</script>

<style lang="scss">
@import "@/scss/app.scss";
</style>
