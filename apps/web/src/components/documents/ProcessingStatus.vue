<template>
  <div class="flex items-center gap-2">
    <span
      class="inline-flex items-center rounded-full px-2 py-0.5 text-xs font-medium"
      :class="statusClasses"
    >
      <span
        v-if="status === 'processing'"
        class="mr-1.5 h-1.5 w-1.5 animate-pulse rounded-full bg-yellow-500"
      />
      {{ statusLabel }}
    </span>
  </div>
</template>

<script setup lang="ts">
import { computed } from "vue";
import type { DocumentStatus } from "@/types";

const props = defineProps<{
  status: DocumentStatus;
}>();

const statusClasses = computed(() => {
  const classes: Record<string, string> = {
    pending: "bg-gray-100 text-gray-700",
    processing: "bg-yellow-100 text-yellow-700",
    completed: "bg-green-100 text-green-700",
    failed: "bg-red-100 text-red-700",
  };
  return classes[props.status] || classes.pending;
});

const statusLabel = computed(() => {
  const labels: Record<string, string> = {
    pending: "Pending",
    processing: "Processing",
    completed: "Ready",
    failed: "Failed",
  };
  return labels[props.status] || "Unknown";
});
</script>
