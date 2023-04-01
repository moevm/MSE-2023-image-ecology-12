import { QueueItemInfo } from "@/types/queue";
import { QueueStatus } from "@/config/queue";
import axios from "axios";
import { baseURL } from "@/api";


export function updateQueueApi(files: string[]){
  axios.post(baseURL + "/queue/update_queue", files, { headers: { 'Content-Type': 'multipart/form-data' } })
    .then(resp => {
      console.log('Queue updated successfully.');
    });
}
export function getQueueInfo(): Promise<QueueItemInfo[]> {
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
}

