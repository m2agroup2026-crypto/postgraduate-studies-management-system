import React from "react";
import Panel from "../../components/ui/Panel";

export default function ResearchAnalyticsPanel({
  analytics = {},
  language,
}) {
  const ar = language === "ar";

  const summary = analytics.summary || {};
  const workflow = analytics.workflow || [];
  const departments = analytics.departments || [];

  return (
    <Panel className="researchAnalyticsPanel">

      <div className="paneltitle">
        <div>
          <span className="panelEyebrow">
            {ar ? "الذكاء الأكاديمي" : "Academic Intelligence"}
          </span>

          <h3>
            {ar
              ? "تحليل منظومة الدراسات العليا"
              : "Postgraduate Research Analytics"}
          </h3>
        </div>
      </div>


      <div className="analyticsMetrics">

        <div>
          <strong>{summary.students || 0}</strong>
          <span>{ar ? "الطلاب" : "Students"}</span>
        </div>

        <div>
          <strong>{summary.theses || 0}</strong>
          <span>{ar ? "الرسائل" : "Theses"}</span>
        </div>

        <div>
          <strong>{summary.defenses || 0}</strong>
          <span>{ar ? "المناقشات" : "Defenses"}</span>
        </div>

      </div>


      <div className="analyticsSection">

        <h4>
          {ar ? "مسار الرسائل العلمية" : "Thesis Pipeline"}
        </h4>

        {workflow.map((item)=>(
          <div className="pipelineRow" key={item.status}>

            <span>
              {ar ? item.label_ar : item.label_en}
            </span>

            <div className="pipelineBar">
              <div
                style={{
                  width:`${Math.min(item.count / 12,100)}%`
                }}
              />
            </div>

            <strong>
              {item.count}
            </strong>

          </div>
        ))}

      </div>


      <div className="analyticsSection">

        <h4>
          {ar ? "أعلى الأقسام نشاطًا" : "Top Departments"}
        </h4>


        {departments.slice(0,5).map((item,index)=>(
          <div className="departmentRow" key={index}>
            <span>
              {item.department__name_ar}
            </span>

            <strong>
              {item.total}
            </strong>
          </div>
        ))}

      </div>


    </Panel>
  );
}
