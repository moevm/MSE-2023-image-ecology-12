<template>
  <div class="container mt-3">
    <div class="m-auto col-10 col-lg-6">
      <button type="button" class="btn btn-success" @click="scheduleTask">
        Запланировать 
      </button>
    </div>
  </div>
</template>

<script setup lang="ts">
import { scheduleTask } from "@/components/routes/scheduler/api";
import { FormKitGroupValue, FormKitNode } from "@formkit/core";
import { useToaster } from "@/store/toaster";
import { ToastTypes } from "@/config/toast";
import { computed, ref } from "vue";

const tiffRegExp = /.(tif|tiff)$/i;

function checkFormat(node: FormKitNode) {
  return (node.value as { name: string }[]).every((f) =>
    tiffRegExp.test(f.name)
  );
}

const toaster = useToaster();

const files = ref<{ name: string; file: File }[]>([]);

const namesSchema = computed(() =>
  files.value.map((f) => ({
    $formkit: "text",
    name: f.name,
    label: `Название карты на снимке ${f.name}`,
    validation: "required",
  }))
);

async function submit(data: FormKitGroupValue) {
  try {
    await Promise.all(
      files.value.map((f) =>
      scheduleTask()
      )
    );
  } catch (e) {
    toaster.addToast({
      title: "Информация",
      body: "Не удалось загрузить файлы",
      type: ToastTypes.danger,
    });
  }
}
</script>

<style scoped lang="scss"></style>
