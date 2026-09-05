import React from "react";

export default function AlertsPanel({ alerts = [] }) {
  return (
    <article className="panel">
      <h3>تنبيهات تتطلب إجراء</h3>

      <ul>
        {alerts.length ? (
          alerts.map((alert, index) => (
            <li key={index}>
              <b>{index + 1}</b>
              <span>{alert.text}</span>
            </li>
          ))
        ) : (
          <li>
            لا توجد تنبيهات حالياً.
          </li>
        )}
      </ul>
    </article>
  );
}
