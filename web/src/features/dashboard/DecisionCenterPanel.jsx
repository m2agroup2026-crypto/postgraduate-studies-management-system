import React from "react";
import Panel from "../../components/ui/Panel";

export default function DecisionCenterPanel({
  decisions = [],
  language,
}) {
  const ar = language === "ar";

  const items = decisions.length
    ? decisions
    : [
        {
          title_ar: "لا توجد طلبات تحتاج قرار حاليًا",
          title_en: "No pending decisions currently",
          status_ar: "النظام يعمل بكفاءة",
          status_en: "System operating normally",
        },
      ];

  return (
    <Panel className="decisionCenterPanel">
      <div className="paneltitle">
        <div>
          <span className="panelEyebrow">
            {ar ? "مركز القرارات" : "Decision Center"}
          </span>

          <h3>
            {ar
              ? "الطلبات التي تحتاج إجراء"
              : "Actions Requiring Attention"}
          </h3>
        </div>
      </div>

      <div className="decisionList">
        {items.map((item, index) => (
          <div
            key={index}
            className="decisionItem"
          >
            <div>
              <strong>
                {ar ? item.title_ar : item.title_en}
              </strong>

              <small>
                {ar ? item.status_ar : item.status_en}
              </small>
            </div>
          </div>
        ))}
      </div>
    </Panel>
  );
}
