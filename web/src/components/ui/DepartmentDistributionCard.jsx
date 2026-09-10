import React from "react";

export default function DepartmentDistributionCard({
  label,
  total,
  width,
}) {
  return (
    <div className="departmentRow">
      <span
        className="departmentLabel"
        title={label}
      >
        {label}
      </span>

      <div className="departmentTrack">
        <div
          className="departmentFill"
          style={{ width }}
        />
      </div>

      <strong>{total}</strong>
    </div>
  );
}
