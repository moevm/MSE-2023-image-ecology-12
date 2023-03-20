<template>
  <h2 class="text-center mt-2 text-primary">Просмотр карты №{{ db_id }}</h2>
  <div class="mt-4 row">
    <div class="col-3">
      <ObjectGroupsList :groups="report.groups" />
    </div>
    <div class="col">
      <MapDisplay :id="db_id" />
    </div>
  </div>
</template>

<script setup lang="ts">
import { useRoute } from "vue-router";
import { getReport } from "@/components/routes/map/api";
import ObjectGroupsList from "@/components/common/ObjectGroupsList.vue";
import MapDisplay from "./MapDisplay.vue";

const route = useRoute();
const db_id: string = (route.params.id as string);
const report = await getReport(db_id);
</script>

<style scoped lang="scss"></style>
