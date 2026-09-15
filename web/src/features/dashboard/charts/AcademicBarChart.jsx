import React from "react";

export default function AcademicBarChart({ data = [], labelFor, valueFor, language = "ar", emptyLabel }) {
  const rows = data
    .map((item) => ({ item, value: Math.max(Number(valueFor(item)) || 0, 0) }))
    .filter((row) => row.value > 0);
  const max = Math.max(...rows.map((row) => row.value), 1);

  if (!rows.length) {
    return <div className="chartEmpty">{emptyLabel || (language === "ar" ? "لا توجد بيانات متاحة." : "No data is available.")}</div>;
  }

  return (
    <div className="academicBarChart" role="img" aria-label={language === "ar" ? "رسم بياني للبيانات الأكاديمية" : "Academic data chart"}>
      {rows.map(({ item, value }, index) => (
        <div className="academicBarRow" key={item.code || item.level || item.status || index}>
          <span title={labelFor(item)}>{labelFor(item) || "—"}</span>
          <div className="academicBarTrack" aria-hidden="true">
            <i style={{ "--bar-size": `${(value / max) * 100}%`, "--bar-delay": `${index * 70}ms` }} />
          </div>
          <strong>{value}</strong>
        </div>
      ))}
    </div>
  );
}
