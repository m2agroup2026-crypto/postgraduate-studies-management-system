import React from "react";
import { Clock3, Landmark, ShieldCheck } from "lucide-react";

import AlertsPanel from "./AlertsPanel";
import DepartmentOverview from "./DepartmentOverview";
import MetricsCards from "./MetricsCards";
import AcademicStructurePanel from "./AcademicStructurePanel";
import RecentStudentFiles from "./RecentStudentFiles";

export default function Dashboard({ data, language, onNavigate }) {
  const ar = language === "ar";
  const pendingMetric = data.ui?.metrics?.find((item) => item.key === "pending");

  return (
    <div className="executiveDashboard">
      <section className="executiveHero">
        <div className="executiveHeroCopy">
          <span className="executiveEyebrow">
            <Landmark size={16} />
            {ar ? "مركز القيادة الأكاديمي التنفيذي" : "Executive academic command center"}
          </span>
          <h2>
            {ar ? data.identity?.name : "Prof. Dr. Mohamed Abdel Baset Khalaf"}
          </h2>
          <p>
            {ar ? data.identity?.title : "Vice Dean for Postgraduate Studies and Research"}
          </p>
          <div className="executiveTrust">
            <ShieldCheck size={17} />
            <span>{ar ? "بيانات مباشرة وفق صلاحيات الحساب" : "Live, permission-scoped data"}</span>
          </div>
        </div>
        <div className="decisionBrief" aria-label={ar ? "ملخص القرار الحالي" : "Current decision brief"}>
          <Clock3 size={22} />
          <span>{pendingMetric?.label_ar || (ar ? "طلبات تنتظر قرارك" : "Awaiting your decision")}</span>
          <strong>{data.metrics?.pending ?? 0}</strong>
          <small>{ar ? "من سير العمل الفعلي" : "From the live workflow"}</small>
        </div>
      </section>

      <MetricsCards
        metrics={data.metrics}
        config={data.ui?.metrics}
        definitions={data.metric_definitions}
        language={language}
      />

      <AcademicStructurePanel
        structure={data.academic_structure}
        language={language}
      />

      <RecentStudentFiles
        records={data.recent_students || []}
        language={language}
        onOpenAll={() => onNavigate?.("students")}
      />

      <div className="grid">
        <DepartmentOverview departments={data.departments}  language={language} />
        <AlertsPanel alerts={data.alerts}  language={language} />
      </div>
    </div>
  );
}
