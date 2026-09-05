import React from "react";

import MetricsCards from "./MetricsCards";
import DepartmentOverview from "./DepartmentOverview";
import AlertsPanel from "./AlertsPanel";

export default function Dashboard({ data }) {
  return (
    <>
      <MetricsCards metrics={data.metrics} />

      <div className="grid">
        <DepartmentOverview
          departments={data.departments}
        />

        <AlertsPanel
          alerts={data.alerts}
        />
      </div>
    </>
  );
}
