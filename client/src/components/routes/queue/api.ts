import { QueueItemInfo } from "@/types/queue";
import { QueueStatus } from "@/config/queue";
import axios from "axios";
import { api } from "@/api";

export function higherQueueApi(id: string){
  const formData = new FormData();
  formData.append("db_id", id);
  return api.post("/queue/higher", formData);
}

export function lowerQueueApi(id: string){
  const formData = new FormData();
  formData.append("db_id", id);
  return api.post("/queue/lower", formData);
}

export function upQueueApi(id: string){
  const formData = new FormData();
  formData.append("db_id", id);
  return api.post("/queue/up", formData);
}

export function downQueueApi(id: string){
  const formData = new FormData();
  formData.append("db_id", id);
  return api.post("/queue/down", formData);
}

export function getQueueInfo(): Promise<QueueItemInfo[]> {
  return  api.get<QueueItemInfo[]>("/queue/get_queue").then(function (res) {
            return res.data;
        })
}

/*export function getQueueInfo(): Promise<QueueItemInfo[]> {
  return Promise.resolve([
    {
      id: "1",
      uploadDate: "2023-02-20T12:10:09",
      progress: 90,
      status: QueueStatus.processing,
      name: "Лес 5",
    },
    {
      id: "2",
      uploadDate: "2023-02-20T13:20:04",
      progress: 0,
      status: QueueStatus.enqueued,
      name: "Лес 6",
    },
    {
      id: "3",
      uploadDate: "2023-02-20T14:43:29",
      progress: 30,
      status: QueueStatus.stopped,
      name: "Лес 7",
    },
    {
      id: "4",
      uploadDate: "2023-02-20T15:36:39",
      progress: 50,
      status: QueueStatus.enqueued,
      name: "Лес 8",
    },
    {
      id: "5",
      uploadDate: "2023-02-20T12:53:02",
      progress: 0,
      status: QueueStatus.enqueued,
      name: "Лес 9",
    },
  ]);
}*/

