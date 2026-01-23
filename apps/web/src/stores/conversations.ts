import { defineStore } from "pinia";
import { ref, computed } from "vue";
import api from "@/api";
import type { Conversation, Message } from "@/types";

export const useConversationsStore = defineStore("conversations", () => {
  const conversations = ref<Conversation[]>([]);
  const currentConversation = ref<Conversation | null>(null);
  const loading = ref(false);
  const asking = ref(false);
  const error = ref<string | null>(null);
  const streamingContent = ref("");

  const messages = computed(() => currentConversation.value?.messages || []);

  async function fetchConversations() {
    loading.value = true;
    error.value = null;
    try {
      const response = await api.conversations.list();
      conversations.value = response.conversations;
    } catch (e: any) {
      error.value = e.response?.data?.detail || "Failed to fetch conversations";
    } finally {
      loading.value = false;
    }
  }

  async function createConversation() {
    try {
      const conversation = await api.conversations.create();
      conversations.value.unshift(conversation);
      currentConversation.value = conversation;
      return conversation;
    } catch (e: any) {
      error.value = e.response?.data?.detail || "Failed to create conversation";
      throw e;
    }
  }

  async function selectConversation(id: string) {
    loading.value = true;
    error.value = null;
    try {
      const conversation = await api.conversations.get(id);
      currentConversation.value = conversation;
    } catch (e: any) {
      error.value = e.response?.data?.detail || "Failed to load conversation";
    } finally {
      loading.value = false;
    }
  }

  async function deleteConversation(id: string) {
    try {
      await api.conversations.delete(id);
      conversations.value = conversations.value.filter((c) => c.id !== id);
      if (currentConversation.value?.id === id) {
        currentConversation.value = null;
      }
    } catch (e: any) {
      error.value = e.response?.data?.detail || "Failed to delete conversation";
    }
  }

  async function askQuestion(question: string) {
    if (!currentConversation.value) return;

    asking.value = true;
    streamingContent.value = "";
    error.value = null;

    const userMessage: Message = {
      id: crypto.randomUUID(),
      conversation_id: currentConversation.value.id,
      role: "user",
      content: question,
      sources: [],
      created_at: new Date().toISOString(),
    };

    if (!currentConversation.value.messages) {
      currentConversation.value.messages = [];
    }
    currentConversation.value.messages.push(userMessage);

    try {
      const response = await api.conversations.ask(currentConversation.value.id, {
        question,
      });

      const assistantMessage: Message = {
        id: crypto.randomUUID(),
        conversation_id: currentConversation.value.id,
        role: "assistant",
        content: response.answer,
        sources: response.sources,
        model_used: response.model_used,
        tokens_used: response.tokens_used,
        created_at: new Date().toISOString(),
      };

      currentConversation.value.messages.push(assistantMessage);

      if (currentConversation.value.title === "New Conversation") {
        currentConversation.value.title = question.slice(0, 80);
      }
    } catch (e: any) {
      error.value = e.response?.data?.detail || "Failed to get answer";
    } finally {
      asking.value = false;
      streamingContent.value = "";
    }
  }

  return {
    conversations,
    currentConversation,
    messages,
    loading,
    asking,
    error,
    streamingContent,
    fetchConversations,
    createConversation,
    selectConversation,
    deleteConversation,
    askQuestion,
  };
});
