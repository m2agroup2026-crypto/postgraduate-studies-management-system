import React from "react";
import AlertsPanel from "./AlertsPanel";
import DepartmentOverview from "./DepartmentOverview";
import MetricsCards from "./MetricsCards";
import AcademicStructurePanel from "./AcademicStructurePanel";
import RecentStudentFiles from "./RecentStudentFiles";
import ExecutiveHero from "../../components/ui/ExecutiveHero";

export default function Dashboard({ data, language, onNavigate }) {
  return (
    <div className="executiveDashboard">
      <ExecutiveHero
        data={data}
        language={language}
      />

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
