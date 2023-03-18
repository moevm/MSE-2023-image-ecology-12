import { QueueStatus } from "@/config/queue";

export interface QueueItemInfo {
  id: number;
  name: string;
  uploadDate: string;
  progress: number;
  status: QueueStatus;
}
