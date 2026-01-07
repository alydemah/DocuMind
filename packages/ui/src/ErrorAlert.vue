<template>
  <div
    class="rounded-lg border border-red-200 bg-red-50 p-4"
    role="alert"
  >
    <div class="flex items-start">
      <svg
        class="mr-3 mt-0.5 h-5 w-5 flex-shrink-0 text-red-500"
        fill="currentColor"
        viewBox="0 0 20 20"
      >
        <path
          fill-rule="evenodd"
          d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z"
          clip-rule="evenodd"
        />
      </svg>
      <div class="flex-1">
        <h3 v-if="title" class="text-sm font-medium text-red-800">{{ title }}</h3>
        <p class="text-sm text-red-700" :class="{ 'mt-1': title }">
          {{ message }}
        </p>
      </div>
      <button
        v-if="dismissible"
        class="ml-3 text-red-400 hover:text-red-600"
        @click="$emit('dismiss')"
      >
        <svg class="h-4 w-4" fill="currentColor" viewBox="0 0 20 20">
          <path
            fill-rule="evenodd"
            d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z"
            clip-rule="evenodd"
          />
        </svg>
      </button>
    </div>
  </div>
</template>

<script setup lang="ts">
withDefaults(
  defineProps<{
    message: string;
    title?: string;
    dismissible?: boolean;
  }>(),
  { dismissible: false }
);

defineEmits<{
  dismiss: [];
}>();
</script>
