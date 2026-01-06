import type { AxiosInstance } from "axios";
import type {
  Conversation,
  AskRequest,
  AskResponse,
  ConversationListResponse,
} from "./types";

export class ConversationsAPI {
  constructor(private http: AxiosInstance) {}

  async create(): Promise<Conversation> {
    const { data } = await this.http.post<Conversation>("/api/v1/conversations");
    return data;
  }

  async list(): Promise<ConversationListResponse> {
    const { data } = await this.http.get<ConversationListResponse>(
      "/api/v1/conversations"
    );
    return data;
  }

  async get(id: string): Promise<Conversation> {
    const { data } = await this.http.get<Conversation>(
      `/api/v1/conversations/${id}`
    );
    return data;
  }

  async delete(id: string): Promise<void> {
    await this.http.delete(`/api/v1/conversations/${id}`);
  }

  async ask(conversationId: string, request: AskRequest): Promise<AskResponse> {
    const { data } = await this.http.post<AskResponse>(
      `/api/v1/conversations/${conversationId}/ask`,
      request
    );
    return data;
  }

  askStream(
    conversationId: string,
    request: AskRequest,
    onChunk: (chunk: string) => void,
    onDone: (response: AskResponse) => void,
    onError: (error: Error) => void
  ): EventSource {
    const url = `${this.http.defaults.baseURL}/api/v1/conversations/${conversationId}/ask`;

    const eventSource = new EventSource(url);

    eventSource.onmessage = (event) => {
      const data = JSON.parse(event.data);
      if (data.type === "chunk") {
        onChunk(data.content);
      } else if (data.type === "done") {
        onDone(data);
        eventSource.close();
      }
    };

    eventSource.onerror = (event) => {
      onError(new Error("Stream connection failed"));
      eventSource.close();
    };

    return eventSource;
  }
}
