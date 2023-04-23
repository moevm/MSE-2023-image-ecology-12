<template>
  <div class="container mt-3">
    <div class="m-auto col-10 col-lg-6">
      <FormKit type="form" :actions="false" @submit="submit">
        <FormKit
          name="files"
          type="file"
          accept=".tiff, .tif"
          label="Файл с картой"
          validation="required"
        />
        <FormKit
          name="name"
          type="text"
          label="Название карты"
          validation="required"
        />
        <FormKit
          outer-class="text-end"
          input-class="$reset btn btn-success"
          type="submit"
          label="Загрузить"
        />
      </FormKit>
    </div>
  </div>
</template>

<script setup lang="ts">
import { uploadMap } from "@/components/routes/upload/api";
import { FormKitGroupValue } from "@formkit/core";
import { useToaster } from "@/store/toaster";
import { ToastTypes } from "@/config/toast";

const toaster = useToaster();

async function submit(data: FormKitGroupValue) {
  const files = data.files as { name: string; file: File }[],
    name = data.name as string;
  try {
    await uploadMap(files[0].file, name);
    toaster.addToast({
      title: "Информация",
      body: "Карта загружена успешно",
      type: ToastTypes.success,
    });
  } catch (e) {
    toaster.addToast({
      title: "Информация",
      body: "Не удалось загрузить файл",
      type: ToastTypes.danger,
    });
  }
}
</script>

<style scoped lang="scss"></style>
