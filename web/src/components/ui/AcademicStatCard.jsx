import React from "react";

export default function AcademicStatCard({
  icon: Icon,
  value,
  label,
}) {
  return (
    <div className="academicStat">
      <div className="academicIcon">
        {Icon && <Icon />}
      </div>

      <strong>{value}</strong>

      <span>{label}</span>
    </div>
  );
}
