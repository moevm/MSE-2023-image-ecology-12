<template>
  <Suspense>
    <AnomalyComponent :id="id" />
    <template #fallback>
      <LoadingSpinner />
    </template>
  </Suspense>
</template>

<script setup lang="ts">
import AnomalyComponent from "@/components/routes/anomaly/AnomalyComponent.vue";
import LoadingSpinner from "@/components/common/LoadingSpinner.vue";
defineProps<{ id: string }>();
</script>

<style scoped lang="scss"></style>
