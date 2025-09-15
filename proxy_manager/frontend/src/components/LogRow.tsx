import { ProxyLog } from "@/types/ProxyLog";

interface LogProps {
  log: ProxyLog;
}

export default function LogRow({ log }: LogProps) {
  const statusClass =
    log.status === "CONNECTED"
      ? "connected-status"
      : log.status === "BLOCKED"
      ? "blocked-status"
      : "";

  const rowClass =
    log.status === "CONNECTED"
      ? "request-connected"
      : log.status === "BLOCKED"
      ? "request-blocked"
      : "";

  return (
    <tr key={log.id} className={rowClass}>
      <td className="text-center log-status">
        <div className={`tag ${statusClass}`}>{log.status}</div>
      </td>
      <td className="text-center">{new Date(log.timestamp).toLocaleString()}</td>
      <td className="text-center">{log.client_ip}</td>
      <td className="text-center">
        <div>{log.target_host}</div>
        <div>{log.target_ip}</div>
      </td>
      <td className="break-words max-w-s log-requestData">{log.request_data}</td>
    </tr>
  );
}
