import React from "react";
import Panel from "../../../components/ui/Panel";

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

      <div className="workflowList">
        {workflow.length > 0 ? (
          workflow.map((item, index) => (
            <div
              key={index}
              className="workflowItem"
            >
              <strong>
                {item.label}
              </strong>

              <span>
                {item.value}
              </span>
            </div>
          ))
        ) : (
          <div className="workflowItem">
            <strong>
              {ar
                ? "لا توجد بيانات تشغيلية حالياً"
                : "No operational data available"}
            </strong>
          </div>
        )}
      </div>
    </Panel>
  );
}
