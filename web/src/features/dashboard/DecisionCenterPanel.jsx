import { localized } from "../../i18n";
import React from "react";
import Panel from "../../components/ui/Panel";

export default function DecisionCenterPanel({
  decisions = [],
  language,
}) {
  const ar = language === "ar";

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
        {decisions.length ? decisions.map((item, index) => (
          <div
            key={index}
            className="decisionItem"
          >
            <div>
              <strong>
                {localized(item, "title", language)}
              </strong>

              <small>
                {localized(item, "status", language)}
              </small>
            </div>
          </div>
        )) : (
          <div className="decisionItem">
            <div>
              <strong>{ar ? "لا توجد طلبات تحتاج قرار حاليًا" : "No pending decisions currently"}</strong>
              <small>{ar ? "النظام يعمل بكفاءة" : "System operating normally"}</small>
            </div>
          </div>
        )}
      </div>
    </Panel>
  );
}
