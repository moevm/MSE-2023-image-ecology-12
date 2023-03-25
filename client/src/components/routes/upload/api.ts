export function uploadMap(file: File, name: string) {
  const formData = new FormData();
  formData.append("file", file);
  formData.append("name", name);
  return Promise.resolve(undefined);
}
