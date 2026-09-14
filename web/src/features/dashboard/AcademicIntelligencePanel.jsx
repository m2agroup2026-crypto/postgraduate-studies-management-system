import React from "react";
import Panel from "../../components/ui/Panel";

export default function AcademicIntelligencePanel({
  intelligence = {},
  language,
}) {
  const ar = language === "ar";

  const summary = intelligence.summary || {};
  const degrees = intelligence.degrees_distribution || [];
  const departments = intelligence.top_departments || [];

  return (
    <Panel className="academicIntelligencePanel">
      <div className="intelligenceHeader">
        <h3>
          {ar
            ? "ذكاء الهيكل الأكاديمي"
            : "Academic Intelligence"}
        </h3>

        <span className="statusBadge">
          {ar ? "تحليل مباشر" : "Live Analysis"}
        </span>
      </div>

      <div className="academicSummaryGrid">
        <div>
          <strong>{summary.departments || 0}</strong>
          <span>{ar ? "قسم" : "Departments"}</span>
        </div>

        <div>
          <strong>{summary.programs || 0}</strong>
          <span>{ar ? "برنامج" : "Programs"}</span>
        </div>

        <div>
          <strong>{summary.students || 0}</strong>
          <span>{ar ? "طالب" : "Students"}</span>
        </div>

        <div>
          <strong>{summary.theses || 0}</strong>
          <span>{ar ? "رسالة" : "Theses"}</span>
        </div>
      </div>

      <h4>
        {ar ? "توزيع الدرجات العلمية" : "Degree Distribution"}
      </h4>

      <div className="intelligenceList">
        {degrees.map((item) => (
          <div key={item.level} className="intelligenceRow">
            <span>
              {ar ? localized(item, "name", language) : item.name_en}
            </span>

            <strong>
              {item.programs_count}
            </strong>
          </div>
        ))}
      </div>

      <h4>
        {ar ? "أكثر الأقسام نشاطًا" : "Top Departments"}
      </h4>

      <div className="intelligenceList">
        {departments.map((item, index) => (
          <div
            key={index}
            className="intelligenceRow"
          >
            <span>
              {ar
                ? localizedFlat(item, "department__name", language)
                : item.department__name_en}
            </span>

            <strong>
              {item.students_count}
            </strong>
          </div>
        ))}
      </div>
    </Panel>
  );
}
