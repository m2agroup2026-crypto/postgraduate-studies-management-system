import React from "react";
import Panel from "../../components/ui/Panel";

export default function AlertsPanel({ alerts = [], language = "ar" }) {
  const ar = language === "ar";

  return (
    <Panel className="alertsPanel alertsUnified">
      <div className="paneltitle">
        <h3>{ar ? "تنبيهات تتطلب إجراء" : "Actionable Alerts"}</h3>
      </div>

      <div className="alertsList">
        {alerts.length ? (
          alerts.map((alert, index) => {
            const text = ar
              ? alert.text_ar || alert.text || ""
              : alert.text_en || alert.text || alert.text_ar || "";

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
