import { ref, onBeforeUnmount, onBeforeMount, readonly } from "vue";
import { QueueItemInfo } from "@/types/queue";
import { socket } from "@/api/websocket/index";

const queue = ref<QueueItemInfo[]>([]);
const consumers = ref(0);
const listener = (newQueue: QueueItemInfo[]) => {
  queue.value = newQueue;
};

export const useQueue = () => {
  if (consumers.value === 0) onBeforeMount(() => socket.on("queue", listener));
  consumers.value++;

  onBeforeUnmount(() => {
    consumers.value--;
    if (consumers.value === 0) socket.off("queue");
  });

  return { queue: readonly(queue) };
};
