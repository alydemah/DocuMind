<template>
  <div class="p-6">
    <div class="mx-auto max-w-3xl space-y-8">
      <!-- System Stats -->
      <section v-if="configStore.stats" class="rounded-xl border border-gray-200 bg-white p-6">
        <h2 class="mb-4 text-lg font-semibold text-gray-900">System Stats</h2>
        <div class="grid grid-cols-2 gap-4 sm:grid-cols-4">
          <div class="rounded-lg bg-gray-50 p-4 text-center">
            <p class="text-2xl font-bold text-brand-600">
              {{ configStore.stats.document_count }}
            </p>
            <p class="text-xs text-gray-500">Documents</p>
          </div>
          <div class="rounded-lg bg-gray-50 p-4 text-center">
            <p class="text-2xl font-bold text-brand-600">
              {{ configStore.stats.chunk_count }}
            </p>
            <p class="text-xs text-gray-500">Chunks</p>
          </div>
          <div class="rounded-lg bg-gray-50 p-4 text-center">
            <p class="text-2xl font-bold text-brand-600">
              {{ configStore.stats.vector_count }}
            </p>
            <p class="text-xs text-gray-500">Vectors</p>
          </div>
          <div class="rounded-lg bg-gray-50 p-4 text-center">
            <p class="text-2xl font-bold text-brand-600">
              {{ formatBytes(configStore.stats.storage_used_bytes) }}
            </p>
            <p class="text-xs text-gray-500">Storage</p>
          </div>
        </div>
      </section>

      <!-- LLM Configuration -->
      <section v-if="configStore.config" class="rounded-xl border border-gray-200 bg-white p-6">
        <h2 class="mb-4 text-lg font-semibold text-gray-900">LLM Configuration</h2>
        <div class="space-y-4">
          <div>
            <label class="block text-sm font-medium text-gray-700">Provider</label>
            <select v-model="form.llm_provider" class="input-field mt-1">
              <option value="openai">OpenAI</option>
              <option value="anthropic">Anthropic</option>
              <option value="ollama">Ollama (Local)</option>
            </select>
          </div>
          <div>
            <label class="block text-sm font-medium text-gray-700">Model</label>
            <input v-model="form.llm_model" class="input-field mt-1" />
          </div>
          <div class="grid grid-cols-2 gap-4">
            <div>
              <label class="block text-sm font-medium text-gray-700">Temperature</label>
              <input v-model.number="form.llm_temperature" type="number" step="0.1" min="0" max="2" class="input-field mt-1" />
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700">Max Tokens</label>
              <input v-model.number="form.llm_max_tokens" type="number" min="100" max="8000" class="input-field mt-1" />
            </div>
          </div>
        </div>
      </section>

      <!-- RAG Configuration -->
      <section v-if="configStore.config" class="rounded-xl border border-gray-200 bg-white p-6">
        <h2 class="mb-4 text-lg font-semibold text-gray-900">RAG Settings</h2>
        <div class="grid grid-cols-2 gap-4">
          <div>
            <label class="block text-sm font-medium text-gray-700">Chunk Size</label>
            <input v-model.number="form.rag_chunk_size" type="number" class="input-field mt-1" />
          </div>
          <div>
            <label class="block text-sm font-medium text-gray-700">Chunk Overlap</label>
            <input v-model.number="form.rag_chunk_overlap" type="number" class="input-field mt-1" />
          </div>
          <div>
            <label class="block text-sm font-medium text-gray-700">Top K Results</label>
            <input v-model.number="form.rag_top_k" type="number" min="1" max="20" class="input-field mt-1" />
          </div>
          <div>
            <label class="block text-sm font-medium text-gray-700">Score Threshold</label>
            <input v-model.number="form.rag_score_threshold" type="number" step="0.05" min="0" max="1" class="input-field mt-1" />
          </div>
        </div>
      </section>

      <!-- Save -->
      <div class="flex justify-end">
        <button @click="saveConfig" class="btn-primary" :disabled="saving">
          {{ saving ? 'Saving...' : 'Save Changes' }}
        </button>
      </div>

      <!-- Health -->
      <section v-if="configStore.health" class="rounded-xl border border-gray-200 bg-white p-6">
        <h2 class="mb-4 text-lg font-semibold text-gray-900">Service Health</h2>
        <div class="space-y-2">
          <div v-for="(status, name) in configStore.health.services" :key="name" class="flex items-center justify-between rounded-lg bg-gray-50 px-4 py-2">
            <span class="text-sm font-medium capitalize text-gray-700">{{ name }}</span>
            <span
              class="inline-flex items-center gap-1.5 text-sm"
              :class="status ? 'text-green-600' : 'text-red-600'"
            >
              <span class="h-2 w-2 rounded-full" :class="status ? 'bg-green-500' : 'bg-red-500'" />
              {{ status ? 'Connected' : 'Disconnected' }}
            </span>
          </div>
        </div>
      </section>
    </div>
  </div>
</template>

<script setup lang="ts">
import { onMounted, reactive, ref } from "vue";
import { useConfigStore } from "@/stores/config";

const configStore = useConfigStore();
const saving = ref(false);

const form = reactive({
  llm_provider: "openai",
  llm_model: "gpt-4o-mini",
  llm_temperature: 0.1,
  llm_max_tokens: 2000,
  rag_chunk_size: 1000,
  rag_chunk_overlap: 200,
  rag_top_k: 5,
  rag_score_threshold: 0.7,
});

onMounted(async () => {
  await Promise.all([
    configStore.fetchConfig(),
    configStore.fetchStats(),
    configStore.fetchHealth(),
  ]);

  if (configStore.config) {
    form.llm_provider = configStore.config.llm.provider;
    form.llm_model = configStore.config.llm.model;
    form.llm_temperature = configStore.config.llm.temperature;
    form.llm_max_tokens = configStore.config.llm.max_tokens;
    form.rag_chunk_size = configStore.config.rag.chunk_size;
    form.rag_chunk_overlap = configStore.config.rag.chunk_overlap;
    form.rag_top_k = configStore.config.rag.top_k;
    form.rag_score_threshold = configStore.config.rag.score_threshold;
  }
});

async function saveConfig() {
  saving.value = true;
  try {
    await configStore.updateConfig(form as any);
  } finally {
    saving.value = false;
  }
}

function formatBytes(bytes: number): string {
  if (bytes < 1024) return `${bytes} B`;
  if (bytes < 1024 * 1024) return `${(bytes / 1024).toFixed(0)} KB`;
  if (bytes < 1024 * 1024 * 1024) return `${(bytes / (1024 * 1024)).toFixed(1)} MB`;
  return `${(bytes / (1024 * 1024 * 1024)).toFixed(1)} GB`;
}
</script>
