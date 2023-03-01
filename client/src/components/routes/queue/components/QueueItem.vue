<template>
  <div>
    <div class="row">
      <div class="col-4">Изображение №{{ props.item.id }}</div>
      <div class="col-4">Загружено: {{ props.item.upload }}</div>
      <div class="col-4">
        Время обработки ~ {{ props.item.processingTime }}m
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { defineProps } from "vue";
import { QueueItemObject } from "@/types/queue";

const props = defineProps<{ item: QueueItemObject }>();
</script>

<style scoped lang="scss"></style>
