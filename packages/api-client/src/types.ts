export type {
  Document,
  DocumentChunk,
  DocumentStatus,
  DocumentUploadResponse,
  DocumentListResponse,
  ProcessingStatus,
  Conversation,
  Message,
  Source,
  AskRequest,
  AskResponse,
  ConversationListResponse,
  AppConfig,
  SystemStats,
  HealthStatus,
  LLMConfig,
  EmbeddingConfig,
  RAGConfig,
} from "@documind/shared-types";

export interface ClientOptions {
  baseURL: string;
  timeout?: number;
  headers?: Record<string, string>;
}

export interface PaginationParams {
  page?: number;
  page_size?: number;
}
