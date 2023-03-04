import { QueueItemObject } from "@/types/queue";

export function getQueue(): Promise<QueueItemObject[]> {
  return Promise.resolve([
    { id: 1, upload: "2023-02-20T12:10:09", processingTime: 5 },
    { id: 2, upload: "2023-02-20T13:20:04", processingTime: 2 },
    { id: 3, upload: "2023-02-20T14:43:29", processingTime: 3 },
    { id: 4, upload: "2023-02-20T15:36:39", processingTime: 4 },
    { id: 5, upload: "2023-02-20T12:53:02", processingTime: 1 },
  ]);
}
