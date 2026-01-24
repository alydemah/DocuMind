<template>
  <aside class="flex w-64 flex-col border-r border-gray-200 bg-white">
    <!-- Logo -->
    <div class="flex h-16 items-center gap-2 border-b border-gray-200 px-4">
      <img src="/favicon.svg" alt="DocuMind" class="h-8 w-8" />
      <span class="text-lg font-semibold text-gray-900">DocuMind</span>
    </div>

    <!-- Navigation -->
    <nav class="flex-1 space-y-1 p-3">
      <router-link
        to="/chat"
        class="flex items-center gap-3 rounded-lg px-3 py-2 text-sm font-medium transition-colors"
        :class="
          $route.path.startsWith('/chat')
            ? 'bg-brand-50 text-brand-700'
            : 'text-gray-600 hover:bg-gray-100'
        "
      >
        <svg class="h-5 w-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 10h.01M12 10h.01M16 10h.01M9 16H5a2 2 0 01-2-2V6a2 2 0 012-2h14a2 2 0 012 2v8a2 2 0 01-2 2h-5l-5 5v-5z" />
        </svg>
        Chat
      </router-link>

      <router-link
        to="/documents"
        class="flex items-center gap-3 rounded-lg px-3 py-2 text-sm font-medium transition-colors"
        :class="
          $route.path === '/documents'
            ? 'bg-brand-50 text-brand-700'
            : 'text-gray-600 hover:bg-gray-100'
        "
      >
        <svg class="h-5 w-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
        </svg>
        Documents
      </router-link>

      <router-link
        to="/settings"
        class="flex items-center gap-3 rounded-lg px-3 py-2 text-sm font-medium transition-colors"
        :class="
          $route.path === '/settings'
            ? 'bg-brand-50 text-brand-700'
            : 'text-gray-600 hover:bg-gray-100'
        "
      >
        <svg class="h-5 w-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.066 2.573c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.573 1.066c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.066-2.573c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z" />
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
        </svg>
        Settings
      </router-link>
    </nav>

    <!-- Conversation list -->
    <div class="flex-1 overflow-auto border-t border-gray-200 p-3" v-if="$route.path.startsWith('/chat')">
      <div class="mb-2 flex items-center justify-between">
        <span class="text-xs font-medium uppercase text-gray-500">Conversations</span>
        <button @click="createNew" class="rounded p-1 text-gray-400 hover:bg-gray-100 hover:text-gray-600">
          <svg class="h-4 w-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4" />
          </svg>
        </button>
      </div>

      <div class="space-y-0.5">
        <button
          v-for="conv in conversationsStore.conversations"
          :key="conv.id"
          @click="selectConversation(conv.id)"
          class="w-full rounded-md px-2 py-1.5 text-left text-sm transition-colors"
          :class="
            conversationsStore.currentConversation?.id === conv.id
              ? 'bg-brand-50 text-brand-700'
              : 'text-gray-600 hover:bg-gray-100'
          "
        >
          <span class="block truncate">{{ conv.title || 'New Conversation' }}</span>
        </button>
      </div>
    </div>
  </aside>
</template>

<script setup lang="ts">
import { onMounted } from "vue";
import { useRouter } from "vue-router";
import { useConversationsStore } from "@/stores/conversations";

const router = useRouter();
const conversationsStore = useConversationsStore();

onMounted(() => {
  conversationsStore.fetchConversations();
});

async function createNew() {
  const conv = await conversationsStore.createConversation();
  router.push(`/chat/${conv.id}`);
}

function selectConversation(id: string) {
  conversationsStore.selectConversation(id);
  router.push(`/chat/${id}`);
}
</script>
