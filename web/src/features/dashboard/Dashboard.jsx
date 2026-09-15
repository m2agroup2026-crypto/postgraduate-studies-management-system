import React from "react";
import AlertsPanel from "./AlertsPanel";
import DepartmentOverview from "./DepartmentOverview";
import MetricsCards from "./MetricsCards";
import AcademicStructurePanel from "./AcademicStructurePanel";
import AcademicIntelligencePanel from "./AcademicIntelligencePanel";
import DecisionCenterPanel from "./DecisionCenterPanel";
import ResearchAnalyticsPanel from "./ResearchAnalyticsPanel";
import RecentStudentFiles from "./RecentStudentFiles";
import ExecutiveHero from "../../components/ui/ExecutiveHero";
import DashboardSection from "../../components/ui/DashboardSection";
import AIInsightPanel from "./intelligence/AIInsightPanel";
import WorkflowStatusPanel from "./intelligence/WorkflowStatusPanel";
import RoleCommandDeck from "./RoleCommandDeck";

export default function Dashboard({ data, user, language, onNavigate }) {
  const roles = new Set(user?.roles || data.roles || []);
  const mode = user?.can_manage_dashboard || roles.has("PLATFORM_ADMIN")
    ? "platformDirector"
    : roles.has("VICE_DEAN_POSTGRADUATE") || roles.has("VICE_DEAN")
      ? "viceDean"
      : "academicLeader";

  return (
    <div className={`executiveDashboard ${mode}Dashboard`}>
      <DashboardSection className="executiveOverview">
        <ExecutiveHero
          data={data}
          user={user}
          language={language}
          mode={mode}
        />

        <RoleCommandDeck data={data} user={user} language={language} onNavigate={onNavigate} />

        <MetricsCards
          metrics={data.metrics || {}}
          config={data.ui?.metrics}
          language={language}
        />

        <DecisionCenterPanel
          decisions={data.pending_decisions || []}
          language={language}
        />
      </DashboardSection>

      <DashboardSection className="commandIntelligence">
        <div className="grid commandIntelligenceGrid">
          <AIInsightPanel
            language={language}
            insights={data.ai_insights || []}
          />
          <WorkflowStatusPanel
            language={language}
            workflow={data.research_analytics?.workflow || []}
          />
        </div>
      </DashboardSection>

      <DashboardSection className="academicIntelligence">
        <AcademicStructurePanel
          structure={data.academic_structure || {}}
          language={language}
        />

        <AcademicIntelligencePanel
          intelligence={data.academic_intelligence || {}}
          language={language}
        />

        <ResearchAnalyticsPanel
          analytics={data.research_analytics || {}}
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
