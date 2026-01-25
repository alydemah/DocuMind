<template>
  <div
    class="flex gap-4"
    :class="message.role === 'user' ? 'justify-end' : 'justify-start'"
  >
    <!-- Avatar -->
    <div
      v-if="message.role === 'assistant'"
      class="flex h-8 w-8 flex-shrink-0 items-center justify-center rounded-full bg-brand-100 text-brand-600"
    >
      <svg class="h-4 w-4" fill="currentColor" viewBox="0 0 20 20">
        <path d="M10 2a8 8 0 100 16 8 8 0 000-16zm0 14a6 6 0 110-12 6 6 0 010 12z" />
      </svg>
    </div>

    <div
      class="max-w-[80%] rounded-2xl px-4 py-3"
      :class="
        message.role === 'user'
          ? 'bg-brand-600 text-white'
          : 'bg-white shadow-sm ring-1 ring-gray-200'
      "
    >
      <!-- Content -->
      <div
        v-if="message.role === 'assistant'"
        class="prose prose-sm max-w-none"
        v-html="renderedContent"
      />
      <p v-else class="text-sm">{{ message.content }}</p>

      <!-- Sources -->
      <div v-if="message.sources?.length" class="mt-3 border-t border-gray-100 pt-3">
        <p class="mb-2 text-xs font-medium text-gray-500">Sources</p>
        <div class="space-y-1">
          <SourceCitation
            v-for="(source, idx) in message.sources"
            :key="idx"
            :source="source"
          />
        </div>
      </div>

      <!-- Meta -->
      <div
        v-if="message.role === 'assistant' && message.model_used"
        class="mt-2 text-xs text-gray-400"
      >
        {{ message.model_used }}
        <span v-if="message.tokens_used">
          &middot; {{ message.tokens_used.total }} tokens
        </span>
      </div>
    </div>

    <!-- User avatar -->
    <div
      v-if="message.role === 'user'"
      class="flex h-8 w-8 flex-shrink-0 items-center justify-center rounded-full bg-gray-200 text-gray-600"
    >
      <svg class="h-4 w-4" fill="currentColor" viewBox="0 0 20 20">
        <path fill-rule="evenodd" d="M10 9a3 3 0 100-6 3 3 0 000 6zm-7 9a7 7 0 1114 0H3z" clip-rule="evenodd" />
      </svg>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from "vue";
import { marked } from "marked";
import type { Message } from "@/types";
import SourceCitation from "./SourceCitation.vue";

const props = defineProps<{
  message: Message;
}>();

const renderedContent = computed(() => {
  return marked.parse(props.message.content, { breaks: true });
});
</script>
