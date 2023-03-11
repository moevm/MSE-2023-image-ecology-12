<template>
  <div class="row m-auto gap-1">
    <button
      v-for="action of params.actions"
      v-show="show(action)"
      :key="action.icon + action.tooltip"
      class="btn btn-primary col-auto rounded-circle"
    >
      <i
        v-bs-tooltip.top.html="action.tooltip"
        :class="action.icon"
        @click="action.onClicked(action, params.data)"
      ></i>
    </button>
  </div>
</template>

<script setup lang="ts">
import { ICellRendererParams } from "ag-grid-community";
import { Action } from "@/types/ag-grid/actions";

const props = defineProps<{
  params: ICellRendererParams & { actions: Action[] };
}>();

function show(action: Action) {
  switch (typeof action.hide) {
    case "boolean":
      return !action.hide;
    case "function":
      return !action.hide(props.params.data, props.params.value);
  }
  return true;
}
</script>

<style scoped lang="scss"></style>
