<template>
  <div class="flex items-center justify-center" :class="containerClass">
    <div
      class="animate-spin rounded-full border-2 border-gray-300 border-t-brand-600"
      :class="sizeClass"
    />
    <span v-if="label" class="ml-3 text-sm text-gray-500">{{ label }}</span>
  </div>
</template>

<script setup lang="ts">
import { computed } from "vue";

const props = withDefaults(
  defineProps<{
    size?: "sm" | "md" | "lg";
    label?: string;
  }>(),
  { size: "md" }
);

const sizeClass = computed(() => {
  const sizes = {
    sm: "h-4 w-4",
    md: "h-8 w-8",
    lg: "h-12 w-12",
  };
  return sizes[props.size];
});

const containerClass = computed(() => {
  return props.size === "lg" ? "py-12" : "py-4";
});
</script>
