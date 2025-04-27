'use client';

import { useEffect, useState } from "react";
import SideIconButton from "@/components/SideIconButton";
import ToggleButton from "@/components/ToggleButton";
import axios from "axios";
import "@/styles/pages/settings.css"
import Logs from "@/app/logs/page"

interface StatusResponse {
    proxyActive: boolean;
    blacklistEnabled: boolean;
    logsEnabled: boolean;
}

export default function SettingsPage() {
    const [mounted, setMounted] = useState(false);
    const [proxyActive, setProxyActive] = useState(false);
    const [blacklistEnabled, setBlacklistEnabled] = useState(false);
    const [logsEnabled, setLogsEnabled] = useState(false);

    useEffect(() => {
        setMounted(true);
        fetchStatus();
    }, []);

    const fetchStatus = async () => {
        try {
            const response = await axios.get<StatusResponse>("http://127.0.0.1:8000/proxy/status/");
            const data = response.data;
            setProxyActive(data.proxyActive);
            setBlacklistEnabled(data.blacklistEnabled);
            setLogsEnabled(data.logsEnabled);
        } catch (error) {
            console.error("Error fetching status:", error);
        }
    };

    const updateStatus = async (settings: StatusResponse) => {
        try {
            const response = await axios.post<StatusResponse>("http://127.0.0.1:8000/proxy/control/", settings);
            const data = response.data;
            setProxyActive(data.proxyActive);
            setBlacklistEnabled(data.blacklistEnabled);
            setLogsEnabled(data.logsEnabled);
        } catch (error) {
            console.error("Error updating status:", error);
        }
    };

    const handleProxyToggle = () => {
        updateStatus({
            proxyActive: !proxyActive,
            blacklistEnabled,
            logsEnabled,
        });
    };

    const handleBlacklistToggle = () => {
        updateStatus({
            proxyActive,
            blacklistEnabled: !blacklistEnabled,
            logsEnabled,
        });
    };

    const handleLogsToggle = () => {
        updateStatus({
            proxyActive,
            blacklistEnabled,
            logsEnabled: !logsEnabled,
        });
    };

    if (!mounted) return null;

    return (
        <div className="page gap-5">
            <div className="text-center">
                <h1 className="text-2xl font-bold mb-4">HTTPS Proxy Server</h1>
                <p className="font-bold text-5xl">IP: 0.0.0.0</p>

                <div className="flex items-center justify-center gap-10">                    
                    <p className="text-sub">Proxy: {proxyActive ? "Online" : "Offline"}</p>
                    <p className="text-sub">Blacklist: {blacklistEnabled ? "Enabled" : "Disabled"}</p>
                    <p className="text-sub">Logs: {logsEnabled ? "Enabled" : "Disabled"}</p>
                </div>
            </div>


            <div className="flex gap-5 w-full">
                <div className="w-2/3">
                    <Logs/>
                </div>
            
            
                <div className="panel flex flex-col gap-5 w-1/3 min-w-1xl">

                    <div className="flex items-center justify-between">
                        <div>
                            <p className="text-sub">Proxy Server</p>
                            <p className="text">Start or Stop the server</p>
                        </div>
                        <ToggleButton checked={proxyActive} onChange={handleProxyToggle} />
                    </div>

                    <div className="flex items-center justify-between">
                        <div>
                            <p className={`text-sub`}>Blacklist</p>
                            <p className="text">Enable or disable domain blacklist</p>
                        </div>
                        <ToggleButton checked={blacklistEnabled} onChange={handleBlacklistToggle} />
                    </div>

                    <div className="flex items-center justify-between">
                        <div>
                            <p className="text-sub">Log Storage</p>
                            <p className="text">Start or stop saving new Logs to the Database</p>
                        </div>
                        <ToggleButton checked={logsEnabled} onChange={handleLogsToggle} />
                    </div>
                </div>

                {/* Opcionalmente puedes eliminar estos botones si solo usarás ToggleButtons */}
                {/* <SideIconButton icon="/OnOff.png" text="Start/Stop Proxy" onClick={handleProxyToggle} />
                <button onClick={handleBlacklistToggle}>
                    {blacklistEnabled ? "Disable Blacklist" : "Enable Blacklist"}
                </button>
                <button onClick={handleLogsToggle}>
                    {logsEnabled ? "Disable Logs" : "Enable Logs"}
                </button> */}
            </div>
        </div>
    );
}
