import React from "react";
import Panel from "../../../components/ui/Panel";

export default function SystemHealthPanel({
  language,
}) {
  const ar = language === "ar";

  return (
    <Panel className="systemHealthPanel">
      <div className="intelligenceHeader">
        <h3>
          {ar ? "حالة النظام" : "System Health"}
        </h3>

        <span className="statusBadge">
          {ar ? "يعمل بكفاءة" : "Operational"}
        </span>
      </div>

      <div className="healthGrid">
        <div>
          <strong>99.8%</strong>
          <span>
            {ar ? "استقرار المنصة" : "Platform Stability"}
          </span>
        </div>

        <div>
          <strong>✓</strong>
          <span>
            {ar ? "قاعدة البيانات" : "Database"}
          </span>
        </div>

        <div>
          <strong>✓</strong>
          <span>
            {ar ? "الخدمات البرمجية" : "Services"}
          </span>
        </div>
      </div>
    </Panel>
  );
}
