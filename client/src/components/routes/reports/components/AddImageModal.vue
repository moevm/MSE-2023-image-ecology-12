<template>
  <div :id="id" class="modal fade" tabindex="-1" data-bs-backdrop="static">
    <div class="modal-dialog">
      <div class="modal-content">
        <div class="modal-header">
          <h5 class="modal-title">Загрузка карты</h5>
          <button type="button" class="btn-close" @click="close"></button>
        </div>
        <div class="modal-body">
          <div class="mb-3">
            <input
              id="formFile"
              ref="fileInput"
              class="form-control"
              type="file"
            />
          </div>
        </div>
        <div class="modal-footer">
          <button type="button" class="btn btn-secondary" @click="close">
            Отмена
          </button>
          <button type="button" class="btn btn-primary" @click="upload">
            Загрузить
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { onMounted, ref } from "vue";
import { Modal } from "bootstrap";

const id = "addImageModal";
let modalObject: Modal | null = null;

const fileInput = ref<HTMLInputElement>();

onMounted(() => {
  modalObject = new Modal(`#${id}`);
});

function open() {
  modalObject?.show();
}

function close() {
  modalObject?.hide();
}

function upload() {
  console.log(fileInput.value?.files);
}

defineExpose({ open, close });
</script>

<style scoped lang="scss"></style>
