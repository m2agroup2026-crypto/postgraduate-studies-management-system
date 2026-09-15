import React from "react";
import Panel from "../../components/ui/Panel";
import DepartmentDistributionCard from "../../components/ui/DepartmentDistributionCard";
import SectionHeader from "../../components/ui/SectionHeader";
import { localizedFlat } from "../../i18n";

export default function DepartmentDistributionPanel({
  departments = [],
  language = "ar",
}) {
  const ar = language === "ar";
  const max = Math.max(...departments.map((item) => Number(item.total) || 0), 1);

  return (
    <Panel className="departmentsPanel">
      <SectionHeader
        title={ar ? "توزيع الطلاب على الأقسام" : "Student Distribution by Department"}
      />

      <div className="departmentsList">
        {departments.map((item, index) => {
          const label = localizedFlat(item, "department__name", language);

          const total = Number(item.total) || 0;
          const width = `${Math.max((total / max) * 100, 8)}%`;

          return (
            <DepartmentDistributionCard
              key={index}
              label={label}
              total={total}
              width={width}
            />
          );
        })}
      </div>
    </Panel>
  );
}
