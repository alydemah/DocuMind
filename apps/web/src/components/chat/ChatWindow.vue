<template>
  <div class="flex h-full flex-col">
    <!-- Messages -->
    <div ref="messagesContainer" class="flex-1 overflow-auto px-4 py-6">
      <EmptyState
        v-if="!messages.length && !asking"
        title="Start a conversation"
        description="Upload documents and ask questions about them. DocuMind will find answers with source citations."
      >
        <template #icon>
          <svg class="h-16 w-16" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M8 10h.01M12 10h.01M16 10h.01M9 16H5a2 2 0 01-2-2V6a2 2 0 012-2h14a2 2 0 012 2v8a2 2 0 01-2 2h-5l-5 5v-5z" />
          </svg>
        </template>
      </EmptyState>

      <div v-else class="mx-auto max-w-3xl space-y-6">
        <ChatMessage
          v-for="message in messages"
          :key="message.id"
          :message="message"
        />

        <StreamingIndicator v-if="asking" />
      </div>
    </div>

    <!-- Input -->
    <ChatInput @send="handleSend" :disabled="asking" />
  </div>
</template>

<script setup lang="ts">
import { computed, nextTick, ref, watch } from "vue";
import { EmptyState } from "@documind/ui";
import { useConversationsStore } from "@/stores/conversations";
import ChatMessage from "./ChatMessage.vue";
import ChatInput from "./ChatInput.vue";
import StreamingIndicator from "./StreamingIndicator.vue";

const store = useConversationsStore();
const messagesContainer = ref<HTMLElement | null>(null);

const messages = computed(() => store.messages);
const asking = computed(() => store.asking);

watch(
  () => messages.value.length,
  async () => {
    await nextTick();
    if (messagesContainer.value) {
      messagesContainer.value.scrollTop = messagesContainer.value.scrollHeight;
    }
  }
);

async function handleSend(question: string) {
  if (!store.currentConversation) {
    await store.createConversation();
  }
  await store.askQuestion(question);
}
</script>
