<template>
    <transition name="fade">
        <div class="pt-5 position-fixed top-0 start-0 h-100 w-100" style="background-color: rgba(0, 0, 0, 0.25)">
            <div id="backdrop" @click="backdropClick" class="modal1-dialog h-100 d-flex align-items-center justify-content-center overflow-auto">
                <div class="card px-0 container" :style="(maxwidth != null) ? `max-width: ${maxwidth}` : ''">
                    <div class="card-header h2">
                        <slot name="header"></slot>
                    </div>
                    <div class="card-body">
                        <slot name="body"></slot>
                    </div>
                    <footer class="modal-footer">
                        <slot name="footer"></slot>
                        <button
                            type="button"
                            class="btn btn-danger me-1"
                            @click="cancel"
                            aria-label="Close modal"
                        >
                            Cancel
                        </button>

                        <button
                            type="button"
                            class="btn btn-primary"
                            @click="accept"
                            aria-label="Close modal"
                        >
                            Accept
                        </button>
                    </footer>
                </div>
            </div>
        </div>
    </transition>
</template>

<script setup lang="ts">
import { defineProps, defineEmits } from 'vue';

const props = defineProps({
    maxwidth: {
        type: String,
        required: false,
        default: null
    }
})

const emit = defineEmits(['accept', 'cancel']);

const backdropClick = (event: Event) => {
    if (event.target instanceof Element && event.target.id == 'backdrop') {
        emit("cancel");
    }
}

const cancel = () => {
    emit('cancel');
}

const accept = () => {
    emit('accept');
}
</script>

<style scoped>
.fade-enter-active, .fade-leave-active {
  transition: opacity 0.5s
}
.fade-enter-from, .fade-leave-to{
  opacity: 0
}
</style>