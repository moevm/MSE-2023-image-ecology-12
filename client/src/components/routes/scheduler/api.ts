import { api } from "@/api";

export function scheduleTask() {
  const formData = new FormData();
  // formData.append("image", file);
  // formData.append("name", name);
  return api.post("/scheduler/schedule", formData);
}
