<template>
  <Suspense>
    <MapComponent :id="id" />
    <template #fallback>
      <LoadingSpinner />
    </template>
  </Suspense>
</template>

<script setup lang="ts">
import MapComponent from "@/components/routes/map/MapComponent.vue";
import LoadingSpinner from "@/components/common/LoadingSpinner.vue";

defineProps<{ id: number }>();
</script>

<style scoped lang="scss"></style>
