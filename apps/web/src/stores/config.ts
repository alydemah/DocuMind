import { defineStore } from "pinia";
import { ref } from "vue";
import api from "@/api";
import type { AppConfig, SystemStats, HealthStatus } from "@/types";

export const useConfigStore = defineStore("config", () => {
  const config = ref<AppConfig | null>(null);
  const stats = ref<SystemStats | null>(null);
  const health = ref<HealthStatus | null>(null);
  const loading = ref(false);
  const error = ref<string | null>(null);

  async function fetchConfig() {
    try {
      config.value = await api.getConfig();
    } catch (e: any) {
      error.value = "Failed to fetch configuration";
    }
  }

  async function updateConfig(updates: Partial<AppConfig>) {
    try {
      config.value = await api.updateConfig(updates);
    } catch (e: any) {
      error.value = "Failed to update configuration";
      throw e;
    }
  }

  async function fetchStats() {
    try {
      stats.value = await api.stats();
    } catch (e: any) {
      error.value = "Failed to fetch stats";
    }
  }

  async function fetchHealth() {
    try {
      health.value = await api.health();
    } catch (e: any) {
      error.value = "Failed to check health";
    }
  }

  return {
    config,
    stats,
    health,
    loading,
    error,
    fetchConfig,
    updateConfig,
    fetchStats,
    fetchHealth,
  };
});
