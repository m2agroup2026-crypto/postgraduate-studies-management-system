import React from "react";
import AlertsPanel from "./AlertsPanel";
import DepartmentOverview from "./DepartmentOverview";
import MetricsCards from "./MetricsCards";
import AcademicStructurePanel from "./AcademicStructurePanel";
import RecentStudentFiles from "./RecentStudentFiles";
import ExecutiveHero from "../../components/ui/ExecutiveHero";
import DashboardSection from "../../components/ui/DashboardSection";
import SystemHealthPanel from "./intelligence/SystemHealthPanel";
import AIInsightPanel from "./intelligence/AIInsightPanel";
import WorkflowStatusPanel from "./intelligence/WorkflowStatusPanel";

export default function Dashboard({ data, language, onNavigate }) {
  return (
    <div className="executiveDashboard">
      <DashboardSection className="executiveOverview">
        <ExecutiveHero
          data={data}
          language={language}
        />

        <MetricsCards
          metrics={data.metrics || {}}
          config={data.ui?.metrics}
          language={language}
        />
      </DashboardSection>

      <DashboardSection className="commandIntelligence">
        <div className="grid">
          <SystemHealthPanel
            language={language}
          />

          <AIInsightPanel
            language={language}
            insights={data.ai_insights || []}
          />
        </div>

        <WorkflowStatusPanel
          language={language}
          workflow={data.workflow_status || []}
        />
      </DashboardSection>

      <DashboardSection className="academicIntelligence">
        <AcademicStructurePanel
          structure={data.academic_structure || {}}
          language={language}
        />
      </DashboardSection>

      <DashboardSection className="studentRecords">
        <RecentStudentFiles
          records={data.recent_students || []}
          language={language}
          onOpenAll={() => onNavigate?.("students")}
        />
      </DashboardSection>

      <DashboardSection className="operationalOverview">
        <div className="grid">
          <DepartmentOverview
            departments={data.departments || []}
            language={language}
          />

          <AlertsPanel
            alerts={data.alerts || []}
            language={language}
          />
        </div>
      </DashboardSection>
    </div>
  );
}
