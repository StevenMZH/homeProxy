import "@/styles/ToggleButton.css";

interface ToggleButtonProps {
    checked: boolean;
    onChange: () => void;
}

export default function ToggleButton({ checked, onChange }: ToggleButtonProps) {
    return (
        <label className="switch">
            <input type="checkbox" checked={checked} onChange={onChange} />
            <span className="slider"></span>
        </label>
    );
}
