<template>
  <Suspense>
    <ReportsComponent />
    <template #fallback>
      <LoadingSpinner />
    </template>
  </Suspense>
</template>

<script setup lang="ts">
import ReportsComponent from "@/components/routes/reports/ReportsComponent.vue";
import LoadingSpinner from "@/components/common/LoadingSpinner.vue";
</script>

<style scoped lang="scss"></style>
