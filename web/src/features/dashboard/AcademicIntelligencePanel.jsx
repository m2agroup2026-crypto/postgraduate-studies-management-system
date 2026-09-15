import React from "react";
import Panel from "../../components/ui/Panel";
import AcademicBarChart from "./charts/AcademicBarChart";
import { localized, localizedFlat } from "../../i18n";

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

      <AcademicBarChart
        data={degrees}
        language={language}
        labelFor={(item) => localized(item, "name", language)}
        valueFor={(item) => item.programs_count}
      />

      <h4>
        {ar ? "أكثر الأقسام نشاطًا" : "Top Departments"}
      </h4>

      <AcademicBarChart
        data={departments}
        language={language}
        labelFor={(item) => localizedFlat(item, "department__name", language)}
        valueFor={(item) => item.students_count}
      />
    </Panel>
  );
}
