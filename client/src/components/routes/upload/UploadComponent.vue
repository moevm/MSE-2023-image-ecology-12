<template>
  <div class="container mt-3">
    <div class="m-auto col-10 col-lg-6">
      <FormKit type="form" :actions="false" @submit="submit">
        <FormKit
          name="files"
          type="file"
          accept=".tiff,.jpg,.png"
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

function submit(data: { files: { name: string; file: File }[]; name: string }) {
  uploadMap(data.files[0].file, data.name);
}
</script>

<style scoped lang="scss"></style>
