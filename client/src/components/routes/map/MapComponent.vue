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
import { getReport } from "@/components/routes/map/api";
import ObjectGroupsList from "@/components/common/ObjectGroupsList.vue";

const props = defineProps<{ id: number }>();
const report = await getReport(props.id);
</script>

<style scoped lang="scss"></style>
