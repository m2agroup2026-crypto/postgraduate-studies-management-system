import React from "react";

import AlertsPanel from "./AlertsPanel";
import DepartmentOverview from "./DepartmentOverview";
import MetricsCards from "./MetricsCards";

export default function Dashboard({ data, language }) {
  return (
    <>
      <MetricsCards
        metrics={data.metrics}
        config={data.ui?.metrics}
        language={language}
      />

      <div className="grid">
        <DepartmentOverview departments={data.departments} />
        <AlertsPanel alerts={data.alerts} />
      </div>
    </>
  );
}
