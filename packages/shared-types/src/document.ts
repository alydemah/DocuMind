export type DocumentStatus = "pending" | "processing" | "completed" | "failed";
export type FileType = "pdf" | "docx" | "txt" | "md";

export interface Document {
  id: string;
  name: string;
  original_name: string;
  file_type: FileType;
  file_size: number;
  file_hash: string;
  status: DocumentStatus;
  chunk_count: number;
  page_count: number;
  error_message?: string;
  metadata: Record<string, unknown>;
  created_at: string;
  updated_at: string;
}

export interface DocumentChunk {
  id: string;
  document_id: string;
  chunk_index: number;
  content: string;
  page_number?: number;
  token_count?: number;
  metadata: Record<string, unknown>;
  created_at: string;
}

export interface DocumentUploadResponse {
  id: string;
  name: string;
  status: DocumentStatus;
  message: string;
}

export interface DocumentListResponse {
  documents: Document[];
  total: number;
  page: number;
  page_size: number;
}

export interface ProcessingStatus {
  document_id: string;
  status: DocumentStatus;
  progress: number;
  current_step: string;
  error_message?: string;
}
