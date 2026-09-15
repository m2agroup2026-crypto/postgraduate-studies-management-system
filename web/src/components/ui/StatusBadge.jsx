import React from "react";

const supportedTones = new Set(["success", "warning", "danger", "info", "neutral"]);

export default function StatusBadge({ tone = "neutral", status, children, className = "" }) {
  const normalizedTone = String(status || tone).toLowerCase();
  const safeTone = supportedTones.has(normalizedTone) ? normalizedTone : "neutral";

  return (
    <span className={`statusBadge statusBadge--${safeTone} ${className}`.trim()}>
      {children}
    </span>
  );
}
