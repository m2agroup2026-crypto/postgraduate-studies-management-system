import React from "react";
import { localized } from "../../../i18n";

const COLORS = ["#0f766e", "#1d4f75", "#c39a4a", "#5b7f91", "#6f5a8a", "#4d8b68"];

export default function AcademicDonutChart({ data = [], language = "ar", title }) {
  const values = data.map((item) => Math.max(Number(item.count) || 0, 0));
  const total = values.reduce((sum, value) => sum + value, 0);
  const radius = 54;
  const circumference = 2 * Math.PI * radius;
  let offset = 0;

  if (!total) {
    return <div className="chartEmpty">{language === "ar" ? "لا توجد بيانات كافية للرسم." : "No chart data is available."}</div>;
  }

  return (
    <figure className="academicChart donutChart" aria-label={title}>
      <svg viewBox="0 0 160 160" role="img">
        <title>{title}</title>
        <circle className="donutTrack" cx="80" cy="80" r={radius} />
        {data.map((item, index) => {
          const length = (values[index] / total) * circumference;
          const segment = (
            <circle
              className="donutSegment"
              key={item.status || index}
              cx="80"
              cy="80"
              r={radius}
              stroke={COLORS[index % COLORS.length]}
              strokeDasharray={`${length} ${circumference - length}`}
              strokeDashoffset={-offset}
            />
          );
          offset += length;
          return segment;
        })}
        <text className="donutValue" x="80" y="77" textAnchor="middle">{total}</text>
        <text className="donutLabel" x="80" y="96" textAnchor="middle">{language === "ar" ? "رسالة" : "theses"}</text>
      </svg>
      <figcaption className="chartLegend">
        {data.map((item, index) => (
          <span key={item.status || index}>
            <i style={{ background: COLORS[index % COLORS.length] }} />
            <b>{localized(item, "label", language)}</b>
            <strong>{values[index]}</strong>
          </span>
        ))}
      </figcaption>
    </figure>
  );
}
