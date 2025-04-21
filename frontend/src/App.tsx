import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import HomePage from "./pages/HomePage";
import LogsPage from "./pages/SettingsPage";
import SettingsPage from "./pages/SettingsPage";
import NotFoundPage from "./pages/NotFoundPage";
import "./App.css";

function App() {
    return (
        <main>
            <Router>
                <Routes>
                    <Route path="/" element={<HomePage />} />
                    <Route path="/logs" element={<LogsPage />} />
                    <Route path="/settings" element={<SettingsPage />} />
                    <Route path="*" element={<NotFoundPage />} />
                </Routes>
            </Router>
        </main>
    );
}

export default App;
