<template>
  <div class="toast-container position-fixed bottom-0 end-0 p-3">
    <div v-for="toast of toasts" :key="toast.id" class="toast" role="alert">
      <div class="toast-header">
        <span class="me-auto">{{ toast.title }}</span>
        <button
          type="button"
          class="btn-close"
          data-bs-dismiss="toast"
          aria-label="Close"
        />
      </div>
      <div class="toast-body">
        {{ toast.body }}
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from "vue";
import { Toast } from "bootstrap";
import { useToaster } from "@/store/toaster";
import { ToastData } from "@/types/toast";

const { toasts, deleteToast } = useToaster();

function toastHidden(toast: ToastData) {
  console.log("hidden");
}
</script>

<style scoped lang="scss"></style>
