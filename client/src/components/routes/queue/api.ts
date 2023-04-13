import { QueueItemInfo } from "@/types/queue";
import { api } from "@/api";

export function higherQueueApi(id: string){
  return api.put("/queue/higher/" + id);
}

export function lowerQueueApi(id: string){
  return api.put("/queue/lower/" + id);
}

export function upQueueApi(id: string){
  return api.put("/queue/up/" + id);
}

export function downQueueApi(id: string){
  return api.put("/queue/down/" + id);
}

export async function getQueueInfo(): Promise<QueueItemInfo[]> {
  return (await api.get<QueueItemInfo[]>("/queue/get_queue")).data
}

