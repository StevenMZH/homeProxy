import { useEffect, useState } from "react";
import SideIconButton from "../components/SideIconButton";
import axios from "axios";

interface StatusResponse {
    proxyActive: boolean;
    blacklistEnabled: boolean;
    logsEnabled: boolean;
}

function SettingsPage() {
    const [proxyActive, setProxyActive] = useState<boolean>(false);
    const [blacklistEnabled, setBlacklistEnabled] = useState<boolean>(false);
    const [logsEnabled, setLogsEnabled] = useState<boolean>(false);

    // Fetch the current status of all 3 settings
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

    // Update the status with the toggled settings
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

    useEffect(() => {
        fetchStatus();
    }, []);

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

    return (
        <div className="page">
            <h2>Proxy Settings</h2>

            <h3>Proxy is {proxyActive ? "Online" : "Offline"}</h3>
            <h3>Blacklist is {blacklistEnabled ? "Enabled" : "Disabled"}</h3>
            <h3>Logs are {logsEnabled ? "Enabled" : "Disabled"}</h3>

            <SideIconButton icon="OnOff.png" text="Start/Stop Proxy" onClick={handleProxyToggle} />
            <button onClick={handleBlacklistToggle}>
                {blacklistEnabled ? "Disable Blacklist" : "Enable Blacklist"}
            </button>
            <button onClick={handleLogsToggle}>
                {logsEnabled ? "Disable Logs" : "Enable Logs"}
            </button>
        </div>
    );
}

export default SettingsPage;
