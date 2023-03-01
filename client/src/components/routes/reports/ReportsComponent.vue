<template>
  <section class="container-md mt-3">
    <button class="btn btn-primary" @click="addImageModal?.open()">
      Загрузить карту
    </button>
    <div :id="accordionId" class="accordion mt-3">
      <ReportListItem
        v-for="report of reports"
        :key="report.id"
        :report="report"
        :parent-id="accordionId"
        class="accordion-item"
      />
    </div>
  </section>
  <AddImageModal ref="addImageModal" />
</template>

<script setup lang="ts">
import ReportListItem from "@/components/routes/reports/components/ReportListItem.vue";
import { Report } from "@/types/reports";
import AddImageModal from "@/components/routes/reports/components/AddImageModal.vue";
import { ref } from "vue";
import { getReportsList } from "@/components/routes/reports/api";

const addImageModal = ref<InstanceType<typeof AddImageModal>>();
const accordionId = "reportsAccordion";

const reports: Report[] = await getReportsList();
</script>

<style scoped lang="scss"></style>
