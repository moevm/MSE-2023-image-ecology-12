<template>
  <h2 class="text-center mt-2 text-primary">Просмотр карты №{{ id }}</h2>
  <div class="mt-4 row">
    <div class="col-3">
      <ObjectGroupsList :groups="report.groups" />
    </div>
    <div class="col">
      <img src="/src/assets/img.png" />
    </div>
  </div>
</template>

<script setup lang="ts">
import { useRoute } from "vue-router";
import { getReport } from "@/components/routes/map/api";
import ObjectGroupsList from "@/components/common/ObjectGroupsList.vue";

const route = useRoute();
const id: number = parseInt(route.params.id as string);
const report = await getReport(id);
</script>

<style scoped lang="scss"></style>
