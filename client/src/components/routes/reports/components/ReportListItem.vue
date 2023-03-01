<template>
  <div>
    <h2 class="accordion-header">
      <button
        class="accordion-button collapsed"
        type="button"
        data-bs-toggle="collapse"
        :data-bs-target="`#${itemId}`"
      >
        Отчёт № {{ props.report.id }}
      </button>
    </h2>
    <div
      :id="itemId"
      class="accordion-collapse collapse"
      :data-bs-parent="parentId"
    >
      <ObjectGroupsList :groups="props.report.groups" />
      <router-link
        :to="{ name: routeNames.Map, params: { id: props.report.id } }"
      >
        <img class="map-preview w-100 py-2 px-4" src="/src/assets/img.png" />
      </router-link>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed, defineProps } from "vue";
import { Report } from "@/types/reports";
import { routeNames } from "@/router";
import ObjectGroupsList from "@/components/common/ObjectGroupsList.vue";

const props = defineProps<{ report: Report; parentId: string }>();

const itemId = computed(() => `reportListItem${props.report.id}`);
</script>

<style scoped lang="scss">
.map-preview {
  height: 300px;
  object-fit: cover;
}
</style>
