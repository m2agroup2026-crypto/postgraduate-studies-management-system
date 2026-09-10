import React from "react";

export default function AcademicDegreeCard({
  name,
  programsCount,
  programsLabel,
}) {
  return (
    <div className="academicCard">
      <strong>{name}</strong>

      <span>
        {programsCount} {programsLabel}
      </span>
    </div>
  );
}
