import React from "react";

import QuickActions from "./components/QuickActions";
import WorkQueue from "./components/WorkQueue";
import UniversalSearch from "./components/UniversalSearch";

import "./workspace.css";

export default function EmployeeWorkspace({
  api,
  language,
  data,
  onNavigate,
}) {
  const ar = language === "ar";

  return (
    <section
      className="employeeWorkspace"
      dir={ar ? "rtl" : "ltr"}
    >
      <header className="workspaceHeader">
        <div>
          <small>
            {ar
              ? "بيئة تشغيل موظفي الدراسات العليا"
              : "Postgraduate Operations Workspace"}
          </small>

          <h1>
            {ar
              ? "مركز إنجاز معاملات الدراسات العليا"
              : "Academic Operations Center"}
          </h1>

          <p>
            {ar
              ? "إدارة ملفات الطلاب والرسائل والإجراءات اليومية من مكان واحد."
              : "Manage student records, theses, and daily academic operations from one workspace."}
          </p>
        </div>
      </header>


      <UniversalSearch
        api={api}
        language={language}
      />


      <QuickActions
        language={language}
        onNavigate={onNavigate}
      />


      <WorkQueue
        api={api}
        language={language}
        data={data}
      />

    </section>
  );
}
