import type { ProcessingStatus } from "./types";

type StatusCallback = (status: ProcessingStatus) => void;
type ErrorCallback = (error: Event) => void;

export class WebSocketClient {
  private baseURL: string;
  private connections: Map<string, WebSocket> = new Map();

  constructor(baseURL: string) {
    this.baseURL = baseURL.replace(/^http/, "ws");
  }

  subscribeToProcessing(
    documentId: string,
    onStatus: StatusCallback,
    onError?: ErrorCallback
  ): () => void {
    const url = `${this.baseURL}/ws/processing/${documentId}`;
    const ws = new WebSocket(url);

    ws.onmessage = (event) => {
      const status: ProcessingStatus = JSON.parse(event.data);
      onStatus(status);
    };

    ws.onerror = (event) => {
      onError?.(event);
    };

    ws.onclose = () => {
      this.connections.delete(documentId);
    };

    this.connections.set(documentId, ws);

    return () => {
      ws.close();
      this.connections.delete(documentId);
    };
  }

  subscribeToChatStream(
    conversationId: string,
    onChunk: (content: string) => void,
    onDone: () => void,
    onError?: ErrorCallback
  ): () => void {
    const url = `${this.baseURL}/ws/chat/${conversationId}`;
    const ws = new WebSocket(url);

    ws.onmessage = (event) => {
      const data = JSON.parse(event.data);
      if (data.type === "chunk") {
        onChunk(data.content);
      } else if (data.type === "done") {
        onDone();
      }
    };

    ws.onerror = (event) => {
      onError?.(event);
    };

    ws.onclose = () => {
      this.connections.delete(conversationId);
    };

    this.connections.set(conversationId, ws);

    return () => {
      ws.close();
      this.connections.delete(conversationId);
    };
  }

  disconnectAll(): void {
    this.connections.forEach((ws) => ws.close());
    this.connections.clear();
  }
}
