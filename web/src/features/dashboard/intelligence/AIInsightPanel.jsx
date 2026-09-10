import React from "react";
import Panel from "../../../components/ui/Panel";

export default function AIInsightPanel({
  language,
  insights = [],
}) {
  const ar = language === "ar";

  return (
    <Panel className="aiInsightPanel">
      <div className="intelligenceHeader">
        <h3>
          {ar
            ? "ذكاء الحوكمة الأكاديمية"
            : "Academic Governance Intelligence"}
        </h3>

        <span className="statusBadge">
          {ar ? "نشط" : "Active"}
        </span>
      </div>

      <div className="insightContent">
        {insights.length > 0 ? (
          insights.map((item, index) => (
            <div
              key={index}
              className="insightItem"
            >
              <span>✦</span>
              <p>{item}</p>
            </div>
          ))
        ) : (
          <div className="insightItem">
            <span>✦</span>
            <p>
              {ar
                ? "لا توجد تحليلات جديدة حالياً"
                : "No new insights available"}
            </p>
          </div>
        )}
      </div>
    </Panel>
  );
}
