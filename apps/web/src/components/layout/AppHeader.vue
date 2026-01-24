<template>
  <header class="flex h-16 items-center justify-between border-b border-gray-200 bg-white px-6">
    <div>
      <h1 class="text-lg font-semibold text-gray-900">
        {{ pageTitle }}
      </h1>
    </div>

    <div class="flex items-center gap-3">
      <div
        v-if="configStore.health"
        class="flex items-center gap-1.5"
      >
        <span
          class="h-2 w-2 rounded-full"
          :class="
            configStore.health.status === 'healthy'
              ? 'bg-green-500'
              : configStore.health.status === 'degraded'
                ? 'bg-yellow-500'
                : 'bg-red-500'
          "
        />
        <span class="text-xs text-gray-500">
          {{ configStore.health.status }}
        </span>
      </div>
    </div>
  </header>
</template>

<script setup lang="ts">
import { computed, onMounted } from "vue";
import { useRoute } from "vue-router";
import { useConfigStore } from "@/stores/config";

const route = useRoute();
const configStore = useConfigStore();

onMounted(() => {
  configStore.fetchHealth();
});

const pageTitle = computed(() => {
  if (route.path.startsWith("/chat")) return "Chat";
  if (route.path === "/documents") return "Documents";
  if (route.path === "/settings") return "Settings";
  return "DocuMind";
});
</script>
