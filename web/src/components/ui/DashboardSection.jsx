import React from "react";

export default function DashboardSection({
  children,
  className = "",
}) {
  return (
    <section className={`dashboardSection ${className}`}>
      {children}
    </section>
  );
}
