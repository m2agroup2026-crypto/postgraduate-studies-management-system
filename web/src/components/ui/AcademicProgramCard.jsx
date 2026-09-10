import React from "react";

export default function AcademicProgramCard({
  name,
  code,
  department,
  degree,
  labels = {},
}) {
  const departmentLabel = labels.department || "Department";
  const degreeLabel = labels.degree || "Degree";

  return (
    <article className="programCard">
      <b title={name}>{name}</b>

      <small title={code}>{code}</small>

      <p title={`${departmentLabel}: ${department}`}>
        {departmentLabel}: {department}
      </p>

      <p title={`${degreeLabel}: ${degree}`}>
        {degreeLabel}: {degree}
      </p>
    </article>
  );
}
