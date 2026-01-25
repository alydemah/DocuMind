<template>
  <div class="border-t border-gray-200 bg-white px-4 py-4">
    <form @submit.prevent="handleSubmit" class="mx-auto flex max-w-3xl gap-3">
      <input
        v-model="question"
        type="text"
        placeholder="Ask a question about your documents..."
        class="input-field flex-1"
        :disabled="disabled"
        @keydown.enter.prevent="handleSubmit"
      />
      <button
        type="submit"
        class="btn-primary"
        :disabled="!question.trim() || disabled"
      >
        <svg class="h-4 w-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 19l9 2-9-18-9 18 9-2zm0 0v-8" />
        </svg>
      </button>
    </form>
  </div>
</template>

<script setup lang="ts">
import { ref } from "vue";

const props = defineProps<{
  disabled?: boolean;
}>();

const emit = defineEmits<{
  send: [question: string];
}>();

const question = ref("");

function handleSubmit() {
  if (!question.value.trim() || props.disabled) return;
  emit("send", question.value.trim());
  question.value = "";
}
</script>
