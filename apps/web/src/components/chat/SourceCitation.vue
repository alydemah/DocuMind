<template>
  <div class="rounded-lg bg-gray-50 p-2 text-xs">
    <div class="flex items-center gap-2">
      <svg class="h-3.5 w-3.5 flex-shrink-0 text-brand-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
      </svg>
      <span class="font-medium text-gray-700">{{ source.document_name }}</span>
      <span v-if="source.page_number" class="text-gray-400">
        p.{{ source.page_number }}
      </span>
      <span class="ml-auto text-gray-400">
        {{ Math.round(source.relevance_score * 100) }}% match
      </span>
    </div>
    <p class="mt-1 line-clamp-2 text-gray-500">{{ source.chunk_text }}</p>
  </div>
</template>

<script setup lang="ts">
import type { Source } from "@/types";

defineProps<{
  source: Source;
}>();
</script>
