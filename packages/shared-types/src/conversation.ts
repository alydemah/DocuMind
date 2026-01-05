export type MessageRole = "user" | "assistant";

export interface Source {
  document_id: string;
  document_name: string;
  page_number?: number;
  chunk_text: string;
  relevance_score: number;
}

export interface TokenUsage {
  prompt: number;
  completion: number;
  total: number;
}

export interface Message {
  id: string;
  conversation_id: string;
  role: MessageRole;
  content: string;
  sources: Source[];
  model_used?: string;
  tokens_used?: TokenUsage;
  created_at: string;
}

export interface Conversation {
  id: string;
  title?: string;
  created_at: string;
  updated_at: string;
  messages?: Message[];
}

export interface AskRequest {
  question: string;
  options?: {
    top_k?: number;
    score_threshold?: number;
    document_filter?: string[];
  };
}

export interface AskResponse {
  answer: string;
  sources: Source[];
  model_used: string;
  tokens_used: TokenUsage;
}

export interface ConversationListResponse {
  conversations: Conversation[];
  total: number;
}
