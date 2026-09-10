import React from "react";

export default function SectionHeader({
  icon: Icon,
  eyebrow,
  title,
  action,
}) {
  return (
    <div className="paneltitle">
      <div>
        {eyebrow && (
          <span className="panelEyebrow">
            {Icon && <Icon size={15} />}
            {eyebrow}
          </span>
        )}

        <h3>{title}</h3>
      </div>

      {action}
    </div>
  );
}
