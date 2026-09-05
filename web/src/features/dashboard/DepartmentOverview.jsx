import React from "react";

export default function DepartmentOverview({ departments = [] }) {
  return (
    <article className="panel">
      <div className="paneltitle">
        <h3>توزيع الطلاب على الأقسام</h3>
      </div>

      {departments.length ? (
        departments.map((department) => (
          <div
            className="progress"
            key={department.department__name_ar}
          >
            <span>
              {department.department__name_ar}
            </span>

            <i>
              <em
                style={{
                  width: Math.min(
                    100,
                    department.total * 10
                  ) + "%",
                }}
              />
            </i>

            <b>
              {department.total}
            </b>
          </div>
        ))
      ) : (
        <p>لا توجد بيانات أقسام بعد.</p>
      )}
    </article>
  );
}
