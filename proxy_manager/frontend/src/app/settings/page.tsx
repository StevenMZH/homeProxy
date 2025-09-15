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
        <div className="page gap-10 ">
            <div className="text-center flex flex-col gap-5">
                <h1 className="text-4xl font-bold mb-4">HTTPS Proxy Admin</h1>

                <div className="flex items-center justify-center gap-10">
                    <div className="flex flex-col justify-center w-36 gap-2">
                        <p className="text-sub2">Proxy:</p>
                        <p className={`tag ${proxyActive ? "enabled" : "disabled"}`}>{proxyActive ? "Online" : "Offline"}</p>                
                    </div>                 
                    <div className="flex flex-col justify-center w-36 gap-2">
                        <p className="text-sub2">Blacklist:</p>
                        <p className={`tag ${blacklistEnabled ? "enabled" : "disabled"}`}>{blacklistEnabled ? "Enabled" : "Disabled"}</p> 
                    </div>   
                    <div className="flex flex-col justify-center w-36 gap-2">
                        <p className="text-sub2">Log Storage:</p>
                        <p className={`tag ${logsEnabled ? "enabled" : "disabled"}`}>{logsEnabled ? "Enabled" : "Disabled"}</p>
                    </div>
                </div>
            </div>


            <div className="flex w-full flex-col gap-10">
                <div className="panel flex flex-col gap-5 w-full">

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

                <div className="w-full">
                    <Logs/>
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
