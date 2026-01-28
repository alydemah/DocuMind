import { ref } from "vue";

export function useStreaming() {
  const content = ref("");
  const isStreaming = ref(false);
  const error = ref<string | null>(null);
  let eventSource: EventSource | null = null;

  function startStream(url: string, body: any) {
    content.value = "";
    isStreaming.value = true;
    error.value = null;

    eventSource = new EventSource(url);

    eventSource.onmessage = (event) => {
      try {
        const data = JSON.parse(event.data);
        if (data.type === "chunk") {
          content.value += data.content;
        } else if (data.type === "done") {
          stopStream();
        }
      } catch {
        content.value += event.data;
      }
    };

    eventSource.onerror = () => {
      error.value = "Stream connection lost";
      stopStream();
    };
  }

  function stopStream() {
    eventSource?.close();
    eventSource = null;
    isStreaming.value = false;
  }

  return { content, isStreaming, error, startStream, stopStream };
}
