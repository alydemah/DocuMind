import { defineStore } from "pinia";
import { ref } from "vue";
import api from "@/api";
import type { Document, DocumentStatus } from "@/types";

export const useDocumentsStore = defineStore("documents", () => {
  const documents = ref<Document[]>([]);
  const total = ref(0);
  const loading = ref(false);
  const uploading = ref(false);
  const error = ref<string | null>(null);

  async function fetchDocuments(page = 1, pageSize = 20) {
    loading.value = true;
    error.value = null;
    try {
      const response = await api.documents.list({ page, page_size: pageSize });
      documents.value = response.documents;
      total.value = response.total;
    } catch (e: any) {
      error.value = e.response?.data?.detail || "Failed to fetch documents";
    } finally {
      loading.value = false;
    }
  }

  async function uploadDocument(file: File) {
    uploading.value = true;
    error.value = null;
    try {
      const response = await api.documents.upload(file);
      await fetchDocuments();
      return response;
    } catch (e: any) {
      error.value = e.response?.data?.detail || "Failed to upload document";
      throw e;
    } finally {
      uploading.value = false;
    }
  }

  async function deleteDocument(id: string) {
    try {
      await api.documents.delete(id);
      documents.value = documents.value.filter((d) => d.id !== id);
      total.value--;
    } catch (e: any) {
      error.value = e.response?.data?.detail || "Failed to delete document";
      throw e;
    }
  }

  function updateDocumentStatus(id: string, status: DocumentStatus) {
    const doc = documents.value.find((d) => d.id === id);
    if (doc) {
      doc.status = status;
    }
  }

  return {
    documents,
    total,
    loading,
    uploading,
    error,
    fetchDocuments,
    uploadDocument,
    deleteDocument,
    updateDocumentStatus,
  };
});
