import React from "react";
import AnimatedNumber from "./AnimatedNumber";

export default function MetricCard({
  icon: Icon,
  label,
  value,
  description,
  language = "ar",
}) {
  return (
    <article className="metricCard">
      {Icon && (
        <div className="metricIcon">
          <Icon />
        </div>
      )}

      <span>{label}</span>

      <strong><AnimatedNumber value={value} language={language} /></strong>

      <small>
        {description}
      </small>
    </article>
  );
}
