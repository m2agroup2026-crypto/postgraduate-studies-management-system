import React from "react";

export default function AcademicProgramCard({
  name,
  code,
  department,
  degree,
  labels,
}) {
  return (
    <article className="programCard">
      <b title={name}>{name}</b>

      <small title={code}>{code}</small>

      <p>
        {labels.department}: {department}
      </p>

      <p>
        {labels.degree}: {degree}
      </p>
    </article>
  );
}
