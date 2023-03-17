<template>
  <AnomalyComponent />
</template>

<script setup lang="ts">
import AnomalyComponent from "@/components/routes/anomaly/AnomalyComponent.vue";
defineProps<{ id: number }>();
</script>

<style scoped lang="scss"></style>
