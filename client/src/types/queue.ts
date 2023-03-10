export enum QueueStatus {
  processing = "processing",
  stopped = "paused",
  enqueued = "enqueued",
}

export interface QueueItemInfo {
  id: number;
  upload: string;
  progress: number;
  status: QueueStatus;
}
