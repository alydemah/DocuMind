import { ref, onUnmounted } from "vue";

export function useWebSocket(url: string) {
  const data = ref<any>(null);
  const connected = ref(false);
  const error = ref<string | null>(null);
  let ws: WebSocket | null = null;

  function connect() {
    const wsUrl = url.replace(/^http/, "ws");
    ws = new WebSocket(wsUrl);

    ws.onopen = () => {
      connected.value = true;
      error.value = null;
    };

    ws.onmessage = (event) => {
      try {
        data.value = JSON.parse(event.data);
      } catch {
        data.value = event.data;
      }
    };

    ws.onerror = () => {
      error.value = "WebSocket connection failed";
    };

    ws.onclose = () => {
      connected.value = false;
    };
  }

  function disconnect() {
    ws?.close();
    ws = null;
    connected.value = false;
  }

  function send(message: any) {
    if (ws?.readyState === WebSocket.OPEN) {
      ws.send(typeof message === "string" ? message : JSON.stringify(message));
    }
  }

  onUnmounted(() => {
    disconnect();
  });

  return { data, connected, error, connect, disconnect, send };
}
