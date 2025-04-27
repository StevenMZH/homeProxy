"use client";
import { useState, useEffect } from "react";
import useProxyLogs from "@/hooks/useProxyLogs";
import LogRow from "@/components/LogRow";

export default function LogsPage() {
  const { logs, setLogs, loading } = useProxyLogs();
  const [deleting, setDeleting] = useState<boolean>(false);

  const handleDeleteLogs = () => {
    if (!window.confirm("¿Seguro que deseas borrar todos los logs?")) return;

    setDeleting(true);
    fetch("http://127.0.0.1:8000/proxy/logs/", {
      method: "DELETE",
    })
      .then((res) => {
        if (res.ok) setLogs([]);
        else console.error("Error deleting logs");
      })
      .catch((err) => console.error("Error deleting logs:", err))
      .finally(() => setDeleting(false));
  };

  return (
    <div className="">
      <div className="flex items-center justify-between mb-4">
        <h1 className="text-2xl font-bold">Proxy Logs Dashboard</h1>
        <button
          onClick={handleDeleteLogs}
          className="bg-red-500 hover:bg-red-700 text-white font-semibold px-2 py-1 rounded-lg"
          disabled={deleting}
        >
          {deleting ? "Borrando..." : "Borrar Logs"}
        </button>
      </div>

      {loading ? (
        <p>Loading logs...</p>
      ) : logs.length === 0 ? (
        <p>No logs available.</p>
      ) : (
        <div className="panel">
          <div className="overflow-x-auto overflow-y-auto">
            <table className="min-w-full">
              <thead>
                <tr className="rounded">
                  <th className="log-status">Status</th>
                  <th>Timestamp</th>
                  <th>Client IP</th>
                  <th>Target Host</th>
                  <th className="log-requestData">Request Data</th>
                </tr>
              </thead>
              <tbody>
                {logs.map((log) => (
                  <LogRow key={log.id} log={log} />
                ))}
              </tbody>
            </table>
          </div>
        </div>
      )}
    </div>
  );
}
