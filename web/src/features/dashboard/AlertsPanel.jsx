import React from "react";
import Panel from "../../components/ui/Panel";
import SectionHeader from "../../components/ui/SectionHeader";
import { localized } from "../../i18n";

export default function AlertsPanel({ alerts = [], language = "ar" }) {
  const ar = language === "ar";

  return (
    <Panel className="alertsPanel alertsUnified">
      <SectionHeader
        title={ar ? "تنبيهات تتطلب إجراء" : "Actionable Alerts"}
      />

      <div className="alertsList">
        {alerts.length ? (
          alerts.map((alert, index) => {
            const text = localized(alert, "text", language);

            return (
              <div
                key={index}
                className={`alertRow ${alert.level || "info"}`}
                title={text}
              >
                <span className="alertDot" />
                <p>{text}</p>
              </div>
            );
          })
        ) : (
          <div className="alertRow empty">
            <span className="alertDot" />
            <p>{ar ? "لا توجد تنبيهات حاليًا" : "No alerts at the moment"}</p>
          </div>
        )}
      </div>
    </Panel>
  );
}
