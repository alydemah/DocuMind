<template>
  <div class="rounded-xl border border-gray-200 bg-white p-4 shadow-sm transition-shadow hover:shadow-md">
    <div class="flex items-start justify-between">
      <div class="flex items-center gap-3">
        <div class="rounded-lg bg-brand-50 p-2">
          <svg class="h-5 w-5 text-brand-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
          </svg>
        </div>
        <div>
          <h3 class="text-sm font-medium text-gray-900 line-clamp-1">
            {{ document.name }}
          </h3>
          <p class="text-xs text-gray-500">
            {{ formatFileSize(document.file_size) }}
            &middot;
            {{ document.file_type.toUpperCase() }}
          </p>
        </div>
      </div>

      <button
        @click="$emit('delete', document.id)"
        class="rounded p-1 text-gray-400 hover:bg-red-50 hover:text-red-500"
      >
        <svg class="h-4 w-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
        </svg>
      </button>
    </div>

    <ProcessingStatus :status="document.status" class="mt-3" />

    <div class="mt-3 flex items-center gap-4 text-xs text-gray-500">
      <span v-if="document.chunk_count">
        {{ document.chunk_count }} chunks
      </span>
      <span v-if="document.page_count">
        {{ document.page_count }} pages
      </span>
      <span class="ml-auto">
        {{ formatDate(document.created_at) }}
      </span>
    </div>
  </div>
</template>

<script setup lang="ts">
import type { Document } from "@/types";
import ProcessingStatus from "./ProcessingStatus.vue";

defineProps<{
  document: Document;
}>();

defineEmits<{
  delete: [id: string];
}>();

function formatFileSize(bytes: number): string {
  if (bytes < 1024) return `${bytes} B`;
  if (bytes < 1024 * 1024) return `${(bytes / 1024).toFixed(1)} KB`;
  return `${(bytes / (1024 * 1024)).toFixed(1)} MB`;
}

function formatDate(dateStr: string): string {
  return new Date(dateStr).toLocaleDateString("en-US", {
    month: "short",
    day: "numeric",
  });
}
</script>
