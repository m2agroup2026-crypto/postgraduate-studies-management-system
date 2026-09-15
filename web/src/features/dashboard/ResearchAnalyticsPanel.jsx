import React from "react";
import Panel from "../../components/ui/Panel";
import AnimatedNumber from "../../components/ui/AnimatedNumber";
import AcademicDonutChart from "./charts/AcademicDonutChart";
import AcademicBarChart from "./charts/AcademicBarChart";
import { localizedFlat } from "../../i18n";

export default function ResearchAnalyticsPanel({
  analytics = {},
  language,
}) {
  const ar = language === "ar";

  const summary = analytics.summary || {};
  const workflow = analytics.workflow || [];
  const departments = analytics.departments || [];

  return (
    <Panel className="researchAnalyticsPanel">

      <div className="paneltitle">
        <div>
          <span className="panelEyebrow">
            {ar ? "الذكاء الأكاديمي" : "Academic Intelligence"}
          </span>

          <h3>
            {ar
              ? "تحليل منظومة الدراسات العليا"
              : "Postgraduate Research Analytics"}
          </h3>
        </div>
      </div>


      <div className="analyticsMetrics">

        <div>
          <strong><AnimatedNumber value={summary.students || 0} language={language} /></strong>
          <span>{ar ? "الطلاب" : "Students"}</span>
        </div>

        <div>
          <strong><AnimatedNumber value={summary.theses || 0} language={language} /></strong>
          <span>{ar ? "الرسائل" : "Theses"}</span>
        </div>

        <div>
          <strong><AnimatedNumber value={summary.defenses || 0} language={language} /></strong>
          <span>{ar ? "المناقشات" : "Defenses"}</span>
        </div>

      </div>


      <div className="analyticsSection">

        <h4>
          {ar ? "مسار الرسائل العلمية" : "Thesis Pipeline"}
        </h4>

        <AcademicDonutChart
          data={workflow}
          language={language}
          title={ar ? "توزيع الرسائل حسب مرحلة سير العمل" : "Theses by workflow stage"}
        />

      </div>


      <div className="analyticsSection">

        <h4>
          {ar ? "أعلى الأقسام نشاطًا" : "Top Departments"}
        </h4>


        <AcademicBarChart
          data={departments.slice(0, 5)}
          language={language}
          labelFor={(item) => localizedFlat(item, "department__name", language)}
          valueFor={(item) => item.total}
        />

      </div>


    </Panel>
  );
}
