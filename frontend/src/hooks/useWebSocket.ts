import { useEffect, useRef } from "react";

type OnMessageCallback<T> = (data: T) => void;

export default function useWebSocket<T>(
  url: string,
  onMessage: OnMessageCallback<T>
) {
  const wsRef = useRef<WebSocket | null>(null);

  useEffect(() => {
    const ws = new WebSocket(url);
    wsRef.current = ws;

    ws.onopen = () => console.log("WebSocket connected:", url);
    ws.onmessage = (event) => {
      try {
        const parsed = JSON.parse(event.data);
        onMessage(parsed);
      } catch (err) {
        console.error("WebSocket message parse error:", err);
      }
    };
    ws.onerror = (err) => console.error("WebSocket error:", err);
    ws.onclose = () => console.log("WebSocket disconnected:", url);

    return () => {
      ws.close();
    };
  }, [url, onMessage]);

  return wsRef;
}
