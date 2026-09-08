import React from "react";

export default function AcademicStructurePanel({ structure, language = "ar" }) {
  const ar = language === "ar";

  if (!structure) return null;

  const degrees = structure.degrees || [];
  const programs = structure.programs || [];

  return (
    <section className="panel academicStructure">
      <div className="paneltitle">
        <h3>{ar ? "الهيكل الأكاديمي" : "Academic Structure"}</h3>
      </div>

      <div className="academicDegrees">
        {degrees.map((degree) => (
          <div className="academicCard" key={degree.code}>
            <strong>
              {ar ? degree.name_ar : degree.name_en || degree.name_ar}
            </strong>
            <span>
              {degree.programs_count || 0} {ar ? "برامج" : "Programs"}
            </span>
          </div>
        ))}
      </div>

      <ul>
        {programs.map((program) => (
          <li key={program.code}>
            <b>{program.code}</b>
            <span>
              {ar ? program.name_ar : program.name_en || program.name_ar}
            </span>
            <small>
              {program.degree__name_ar} - {program.department__name_ar}
            </small>
          </li>
        ))}
      </ul>
    </section>
  );
}
