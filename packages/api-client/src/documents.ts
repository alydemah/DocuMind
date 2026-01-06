import type { AxiosInstance } from "axios";
import type {
  Document,
  DocumentChunk,
  DocumentUploadResponse,
  DocumentListResponse,
  PaginationParams,
} from "./types";

export class DocumentsAPI {
  constructor(private http: AxiosInstance) {}

  async upload(file: File): Promise<DocumentUploadResponse> {
    const formData = new FormData();
    formData.append("file", file);

    const { data } = await this.http.post<DocumentUploadResponse>(
      "/api/v1/documents/upload",
      formData,
      { headers: { "Content-Type": "multipart/form-data" } }
    );
    return data;
  }

  async bulkUpload(files: File[]): Promise<DocumentUploadResponse[]> {
    const formData = new FormData();
    files.forEach((file) => formData.append("files", file));

    const { data } = await this.http.post<DocumentUploadResponse[]>(
      "/api/v1/documents/bulk-upload",
      formData,
      { headers: { "Content-Type": "multipart/form-data" } }
    );
    return data;
  }

  async list(params?: PaginationParams): Promise<DocumentListResponse> {
    const { data } = await this.http.get<DocumentListResponse>("/api/v1/documents", {
      params,
    });
    return data;
  }

  async get(id: string): Promise<Document> {
    const { data } = await this.http.get<Document>(`/api/v1/documents/${id}`);
    return data;
  }

  async delete(id: string): Promise<void> {
    await this.http.delete(`/api/v1/documents/${id}`);
  }

  async getChunks(id: string): Promise<DocumentChunk[]> {
    const { data } = await this.http.get<DocumentChunk[]>(
      `/api/v1/documents/${id}/chunks`
    );
    return data;
  }
}
