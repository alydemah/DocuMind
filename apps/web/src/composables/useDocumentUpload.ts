import { ref } from "vue";
import { useDocumentsStore } from "@/stores/documents";

export function useDocumentUpload() {
  const uploading = ref(false);
  const progress = ref(0);
  const error = ref<string | null>(null);
  const store = useDocumentsStore();

  async function upload(files: File[]) {
    uploading.value = true;
    progress.value = 0;
    error.value = null;

    const total = files.length;
    let completed = 0;

    for (const file of files) {
      try {
        await store.uploadDocument(file);
        completed++;
        progress.value = Math.round((completed / total) * 100);
      } catch (e: any) {
        error.value = e.response?.data?.detail || `Failed to upload ${file.name}`;
      }
    }

    uploading.value = false;
  }

  function reset() {
    uploading.value = false;
    progress.value = 0;
    error.value = null;
  }

  return { uploading, progress, error, upload, reset };
}
