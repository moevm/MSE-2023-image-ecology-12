import { ref, onBeforeUnmount, onBeforeMount, readonly } from "vue";
import { MapInfo } from "@/types/maps";
import { getMapsInfo } from "@/components/routes/maps/api";
import { socket } from "@/api/websocket/index";


const images = ref<MapInfo[]>();
const consumers = ref(0);
const listener = (newImages: MapInfo[]) => {
  images.value = newImages;
  console.error('Update map', newImages);
};

export async function useImages() {
  if (consumers.value === 0) onBeforeMount(() => socket.on("images", listener));
  consumers.value++;

  onBeforeUnmount(() => {
    consumers.value--;
    if (consumers.value === 0) socket.off("images");
  });
  
  images.value = await getMapsInfo();
  return { images: readonly(images) };
};
