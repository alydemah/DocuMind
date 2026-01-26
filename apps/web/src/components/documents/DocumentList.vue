<template>
  <div>
    <LoadingSpinner v-if="store.loading" size="lg" label="Loading documents..." />

    <EmptyState
      v-else-if="!store.documents.length"
      title="No documents yet"
      description="Upload your first document to start asking questions."
    />

    <div v-else class="grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
      <DocumentCard
        v-for="doc in store.documents"
        :key="doc.id"
        :document="doc"
        @delete="handleDelete"
      />
    </div>
  </div>
</template>

<script setup lang="ts">
import { onMounted } from "vue";
import { LoadingSpinner, EmptyState } from "@documind/ui";
import { useDocumentsStore } from "@/stores/documents";
import DocumentCard from "./DocumentCard.vue";

const store = useDocumentsStore();

onMounted(() => {
  store.fetchDocuments();
});

async function handleDelete(id: string) {
  if (confirm("Delete this document? This will also remove its vectors.")) {
    await store.deleteDocument(id);
  }
}
</script>
