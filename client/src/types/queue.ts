export enum QueueStatus {
  processing = "processing",
  stopped = "paused",
  enqueued = "enqueued",
}

export interface QueueItemInfo {
  id: number;
  uploadDate: string;
  progress: number;
  status: QueueStatus;
}
