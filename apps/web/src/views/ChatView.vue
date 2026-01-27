<template>
  <div class="h-full">
    <ChatWindow />

    <ErrorAlert
      v-if="conversationsStore.error"
      :message="conversationsStore.error"
      class="fixed bottom-20 left-1/2 z-50 w-96 -translate-x-1/2"
      dismissible
      @dismiss="conversationsStore.error = null"
    />
  </div>
</template>

<script setup lang="ts">
import { onMounted, watch } from "vue";
import { useRoute } from "vue-router";
import { ErrorAlert } from "@documind/ui";
import { useConversationsStore } from "@/stores/conversations";
import ChatWindow from "@/components/chat/ChatWindow.vue";

const route = useRoute();
const conversationsStore = useConversationsStore();

onMounted(() => {
  const id = route.params.id as string;
  if (id) {
    conversationsStore.selectConversation(id);
  }
});

watch(
  () => route.params.id,
  (newId) => {
    if (newId) {
      conversationsStore.selectConversation(newId as string);
    }
  }
);
</script>
