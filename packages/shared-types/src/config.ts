export type LLMProvider = "openai" | "anthropic" | "ollama";
export type EmbeddingProvider = "openai" | "ollama" | "local";

export interface LLMConfig {
  provider: LLMProvider;
  model: string;
  temperature: number;
  max_tokens: number;
  base_url?: string;
}

export interface EmbeddingConfig {
  provider: EmbeddingProvider;
  model: string;
  dimensions: number;
  base_url?: string;
}

export interface RAGConfig {
  chunk_size: number;
  chunk_overlap: number;
  top_k: number;
  score_threshold: number;
}

export interface AppConfig {
  llm: LLMConfig;
  embedding: EmbeddingConfig;
  rag: RAGConfig;
}

export interface SystemStats {
  document_count: number;
  chunk_count: number;
  conversation_count: number;
  storage_used_bytes: number;
  vector_count: number;
}

export interface HealthStatus {
  status: "healthy" | "degraded" | "unhealthy";
  version: string;
  services: {
    database: boolean;
    redis: boolean;
    vector_store: boolean;
    llm_provider: boolean;
  };
}
