import axios, { type AxiosInstance } from "axios";
import { DocumentsAPI } from "./documents";
import { ConversationsAPI } from "./conversations";
import type { ClientOptions, HealthStatus, SystemStats, AppConfig } from "./types";

export class DocuMindClient {
  private http: AxiosInstance;
  public documents: DocumentsAPI;
  public conversations: ConversationsAPI;

  constructor(options: ClientOptions) {
    this.http = axios.create({
      baseURL: options.baseURL,
      timeout: options.timeout ?? 30000,
      headers: {
        "Content-Type": "application/json",
        ...options.headers,
      },
    });

    this.documents = new DocumentsAPI(this.http);
    this.conversations = new ConversationsAPI(this.http);
  }

  async health(): Promise<HealthStatus> {
    const { data } = await this.http.get<HealthStatus>("/api/v1/health");
    return data;
  }

  async stats(): Promise<SystemStats> {
    const { data } = await this.http.get<SystemStats>("/api/v1/stats");
    return data;
  }

  async getConfig(): Promise<AppConfig> {
    const { data } = await this.http.get<AppConfig>("/api/v1/config");
    return data;
  }

  async updateConfig(config: Partial<AppConfig>): Promise<AppConfig> {
    const { data } = await this.http.put<AppConfig>("/api/v1/config", config);
    return data;
  }
}

export function createClient(baseURL: string): DocuMindClient {
  return new DocuMindClient({ baseURL });
}
