import React from "react";

export default function ReportsModule() {
  return (
    <section className="moduleCard" dir="rtl">
      <h2>التقارير الأكاديمية</h2>
      <p>
        مركز التقارير التنفيذية للدراسات العليا.
      </p>

      <div className="metrics">
        <div className="metricCard">
          <strong>تقارير الطلاب</strong>
          <span>عرض بيانات الطلاب المصرح بها</span>
        </div>

        <div className="metricCard">
          <strong>تقارير الرسائل العلمية</strong>
          <span>متابعة حالات الرسائل</span>
        </div>

        <div className="metricCard">
          <strong>تقارير اللجان والمناقشات</strong>
          <span>متابعة الجدول الأكاديمي</span>
        </div>
      </div>
    </section>
  );
}
