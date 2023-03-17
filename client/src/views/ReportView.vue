<template>
  <ReportComponent :id="id" />
</template>

<script setup lang="ts">
import ReportComponent from "@/components/routes/report/ReportComponent.vue";
defineProps<{ id: number }>();
</script>

<style scoped lang="scss"></style>
