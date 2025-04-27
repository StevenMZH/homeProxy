import { useEffect, useState } from "react";

interface ProxyLog {
    id: number;
    timestamp: string;
    client_ip: string;
    target_host: string;
    target_ip: string;
    status: string;
    request_data: string;
}

function LogsPage() {
    const [logs, setLogs] = useState<ProxyLog[]>([]);
    const [loading, setLoading] = useState<boolean>(true);
    const [deleting, setDeleting] = useState<boolean>(false);

    useEffect(() => {
        // Fetch inicial de logs existentes
        fetch("http://127.0.0.1:8000/proxy/logs/")
            .then(response => response.json())
            .then(data => {
                setLogs(data);
                setLoading(false);
            })
            .catch(error => {
                console.error("Error fetching logs:", error);
                setLoading(false);
            });
    
        // Establecer conexión WebSocket
        const ws = new WebSocket("ws://127.0.0.1:8000/ws/logs/");
    
        ws.onopen = () => {
            console.log("WebSocket connection established");
        };
    
        ws.onmessage = (event) => {
            const data = JSON.parse(event.data);
            // Solo añadimos un nuevo log, no reemplazamos toda la lista
            setLogs(prevLogs => [data, ...prevLogs]);
        };
    
        ws.onerror = (error) => {
            console.error("WebSocket error:", error);
        };
    
        ws.onclose = () => {
            console.log("WebSocket connection closed");
        };
    
        // Cleanup
        return () => {
            ws.close();
        };
    }, []);
    

    const handleDeleteLogs = () => {
        if (!window.confirm("¿Seguro que deseas borrar todos los logs?")) return;
        
        setDeleting(true);
        fetch("http://127.0.0.1:8000/proxy/logs/", {
            method: "DELETE",
        })
            .then(response => {
                if (response.ok) {
                    setLogs([]);
                } else {
                    console.error("Error deleting logs");
                }
            })
            .catch(error => console.error("Error deleting logs:", error))
            .finally(() => setDeleting(false));
    };

    return (
        <div className="page p-6">
            <div className="flex items-center justify-between mb-4">
                <h1 className="text-2xl font-bold">Proxy Logs Dashboard</h1>
                <button
                    onClick={handleDeleteLogs}
                    className="bg-red-600 hover:bg-red-700 text-white font-semibold px-4 py-2 rounded-lg"
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
                <div className="overflow-x-auto">
                    <table className="min-w-full bg-white border border-gray-300">
                        <thead>
                            <tr className="bg-gray-100">
                                <th className="">Timestamp</th>
                                <th className="">Client IP</th>
                                <th className="">Target Host</th>
                                <th className="">Target IP</th>
                                <th className="">Status</th>
                                <th className="">Request Data</th>
                            </tr>
                        </thead>
                        <tbody>
                            {logs.map((log) => (
                                <tr key={log.id} className="hover:bg-gray-50">
                                    <td className="">{new Date(log.timestamp).toLocaleString()}</td>
                                    <td className="">{log.client_ip}</td>
                                    <td className="">{log.target_host}</td>
                                    <td className="">{log.target_ip}</td>
                                    <td className="">{log.status}</td>
                                    <td className=" break-words max-w-xs">{log.request_data}</td>
                                </tr>
                            ))}
                        </tbody>
                    </table>
                </div>
            )}
        </div>
    );
}

export default LogsPage;
