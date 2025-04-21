import React from 'react';

interface SideIconButton_Props {
  icon: string;
  text: string;
  onClick: () => void;
}

const SideIconButton: React.FC<SideIconButton_Props> = ({ icon, text, onClick }) => {
  return (
    <button className="SideIconButton" onClick={onClick}>
      <img src={icon} alt={text} />
      <p>{text}</p>
    </button>
  );
};

export default SideIconButton;
