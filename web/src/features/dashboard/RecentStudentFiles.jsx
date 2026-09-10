import React from "react";
import { ArrowLeft, FolderOpen, GraduationCap } from "lucide-react";

const thesisLabels = {
  REGISTERED: "مسجلة",
  SUBMITTED: "مقدمة للمراجعة",
  UNDER_REVIEW: "قيد المراجعة",
  DIRECTOR_APPROVED: "بانتظار قرار الوكيل",
  VICE_DEAN_APPROVED: "معتمدة من الوكيل",
  DEAN_APPROVED: "معتمدة من العميد",
  FINAL_APPROVED: "معتمدة نهائيًا",
  RETURNED: "معادة للاستكمال",
  REJECTED: "مرفوضة",
  COMPLETED: "مكتملة",
};

export default function RecentStudentFiles({ records, language, onOpenAll }) {
  const ar = language === "ar";

  if (!records.length) return null;

  return (
    <section className="panel studentFilesPanel" aria-labelledby="recent-student-files">
      <div className="paneltitle">
        <div>
          <span className="panelEyebrow"><FolderOpen size={15} /> بيانات مباشرة</span>
          <h3 id="recent-student-files">{ar ? "أحدث ملفات الطلاب" : "Recent student records"}</h3>
        </div>
        <button type="button" onClick={onOpenAll}>
          {ar ? "عرض كل الطلاب" : "View all students"}
          <ArrowLeft size={16} aria-hidden="true" />
        </button>
      </div>

      <div className="studentFilesTable" role="table" aria-label={ar ? "أحدث ملفات الطلاب" : "Recent student records"}>
        {records.map((record) => (
          <article className="studentFileRow" role="row" key={record.id}>
            <span className="studentFileIcon"><GraduationCap size={19} /></span>
            <div className="studentFileIdentity">
              <strong>{record.name_ar}</strong>
              <small>
                {record.university_id} · {record.enrollments_count} {ar ? "قيد أكاديمي" : "enrollments"}
              </small>
            </div>
            <span>{record.department}</span>
            <span>{thesisLabels[record.thesis_status] || (ar ? "لا توجد رسالة مسجلة" : "No registered thesis")}</span>
            <span className="recordSource">{ar ? "من قاعدة البيانات" : "Database record"}</span>
          </article>
        ))}
      </div>
    </section>
  );
}
