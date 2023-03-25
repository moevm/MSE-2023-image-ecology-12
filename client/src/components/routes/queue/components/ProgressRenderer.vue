<template>
  <div
    v-bs-tooltip="`${params.value}%`"
    class="progress col"
    role="progressbar"
  >
    <div class="progress-bar" :style="`width: ${params.value}%`">
      {{ params.value }}%
    </div>
  </div>
</template>

<script setup lang="ts">
import { ICellRendererParams } from "ag-grid-community";

defineProps<{
  params: ICellRendererParams<any, number>;
}>();
</script>

<style scoped lang="scss"></style>
