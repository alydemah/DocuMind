<template>
  <div
    class="rounded-xl border-2 border-dashed p-8 text-center transition-colors"
    :class="
      isDragging
        ? 'border-brand-400 bg-brand-50'
        : 'border-gray-300 hover:border-gray-400'
    "
    @dragover.prevent="isDragging = true"
    @dragleave.prevent="isDragging = false"
    @drop.prevent="handleDrop"
  >
    <input
      ref="fileInput"
      type="file"
      class="hidden"
      :accept="acceptedTypes"
      multiple
      @change="handleFileSelect"
    />

    <svg class="mx-auto h-12 w-12 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12" />
    </svg>

    <p class="mt-4 text-sm text-gray-600">
      <button
        type="button"
        class="font-medium text-brand-600 hover:text-brand-500"
        @click="$refs.fileInput.click()"
      >
        Click to upload
      </button>
      or drag and drop
    </p>
    <p class="mt-1 text-xs text-gray-500">
      PDF, DOCX, TXT, MD up to {{ maxSizeMB }}MB
    </p>

    <div v-if="uploading" class="mt-4">
      <LoadingSpinner size="sm" label="Uploading..." />
    </div>

    <ErrorAlert
      v-if="error"
      :message="error"
      class="mt-4"
      dismissible
      @dismiss="error = null"
    />
  </div>
</template>

<script setup lang="ts">
import { ref } from "vue";
import { LoadingSpinner, ErrorAlert } from "@documind/ui";
import { useDocumentsStore } from "@/stores/documents";

const store = useDocumentsStore();
const fileInput = ref<HTMLInputElement | null>(null);
const isDragging = ref(false);
const uploading = ref(false);
const error = ref<string | null>(null);

const acceptedTypes = ".pdf,.docx,.txt,.md";
const maxSizeMB = 50;

async function handleFiles(files: FileList) {
  uploading.value = true;
  error.value = null;

  for (const file of Array.from(files)) {
    try {
      await store.uploadDocument(file);
    } catch (e: any) {
      error.value = e.response?.data?.detail || `Failed to upload ${file.name}`;
    }
  }

  uploading.value = false;
}

function handleFileSelect(event: Event) {
  const input = event.target as HTMLInputElement;
  if (input.files?.length) {
    handleFiles(input.files);
    input.value = "";
  }
}

function handleDrop(event: DragEvent) {
  isDragging.value = false;
  if (event.dataTransfer?.files?.length) {
    handleFiles(event.dataTransfer.files);
  }
}
</script>
