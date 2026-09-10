import React from "react";

export default function MetricCard({
  icon: Icon,
  label,
  value,
  description,
}) {
  return (
    <article className="metricCard">
      {Icon && (
        <div className="metricIcon">
          <Icon />
        </div>
      )}

      <span>{label}</span>

      <strong>{value}</strong>

      <small>
        {description}
      </small>
    </article>
  );
}
