// src/hooks/useProxyLogs.ts
import { useState, useEffect } from "react";
import { ProxyLog } from "@/types/ProxyLog";
import useWebSocket from "./useWebSocket";

export default function useProxyLogs() {
  const [logs, setLogs] = useState<ProxyLog[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetch("http://127.0.0.1:8000/proxy/logs/")
      .then((res) => res.json())
      .then((data) => {
        setLogs(data);
      })
      .catch((err) => {
        console.error("Error fetching logs:", err);
      })
      .finally(() => setLoading(false));
  }, []);

  useWebSocket<ProxyLog>("ws://127.0.0.1:8000/ws/logs/", (newLog) => {
    setLogs((prevLogs) => [newLog, ...prevLogs]);
  });

  return { logs, setLogs, loading };
}
