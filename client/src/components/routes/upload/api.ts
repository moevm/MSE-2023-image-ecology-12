import axios from "axios";
import { baseURL } from "@/api";

export function uploadMap(file: File, name: string) {
  const formData = new FormData();
  formData.append("file", file);
  formData.append("name", name);
  axios
    .post(baseURL + "/images/upload_image", formData, { headers: { 'Content-Type': 'multipart/form-data' } })
    .then(resp => {
      console.log('File uploaded successfully.');
    });
}
