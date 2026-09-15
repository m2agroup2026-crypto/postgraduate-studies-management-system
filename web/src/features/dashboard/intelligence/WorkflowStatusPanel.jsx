import React from "react";
import Panel from "../../../components/ui/Panel";
import AcademicBarChart from "../charts/AcademicBarChart";
import { localized } from "../../../i18n";

export default function WorkflowStatusPanel({
  language,
  workflow = [],
}) {
  const ar = language === "ar";

  return (
    <Panel className="workflowStatusPanel">
      <div className="intelligenceHeader">
        <h3>
          {ar
            ? "حالة مسارات العمل الأكاديمية"
            : "Academic Workflow Status"}
        </h3>

        <span className="statusBadge">
          {ar ? "مراقبة" : "Monitoring"}
        </span>
      </div>

      <AcademicBarChart
        data={workflow}
        language={language}
        labelFor={(item) => localized(item, "label", language)}
        valueFor={(item) => item.count}
        emptyLabel={ar ? "لا توجد بيانات تشغيلية حاليًا" : "No operational data available"}
      />
    </Panel>
  );
}
