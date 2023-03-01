<template>
  <div v-for="group of props.groups" :key="group.name" class="px-3 py-2">
    <span>{{ group.name }}</span>
    <ul class="list-group mt-1">
      <li
        v-for="object of group.objects"
        :key="object.name + object.coordinates"
        class="list-group-item"
      >
        {{ object.name }} по координатам
        <router-link to="">
          {{ object.coordinates }}
        </router-link>
      </li>
    </ul>
  </div>
</template>

<script setup lang="ts">
import { defineProps } from "vue";
import { MapObjectsGroup } from "@/types/reports";

const props = defineProps<{ groups: MapObjectsGroup[] }>();
</script>

<style scoped lang="scss"></style>
