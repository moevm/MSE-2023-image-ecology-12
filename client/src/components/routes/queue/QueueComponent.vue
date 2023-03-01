<template>
  <section class="container-md">
    <ul class="list-group mt-1">
      <QueueItem
        v-for="image of queue"
        :key="image.id + image.id"
        :item="image"
        class="list-group-item"
      />
    </ul>
  </section>
</template>

<script setup lang="ts">
import { getQueue } from "@/components/routes/queue/api";
import QueueItem from "@/components/routes/queue/components/QueueItem.vue";

const queue = await getQueue();
</script>

<style scoped lang="scss"></style>
