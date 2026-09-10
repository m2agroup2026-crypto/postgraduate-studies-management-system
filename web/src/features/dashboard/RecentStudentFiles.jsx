import React from "react";
import { ArrowLeft, FolderOpen } from "lucide-react";
import SectionHeader from "../../components/ui/SectionHeader";
import StudentFileCard from "../../components/ui/StudentFileCard";

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
      <SectionHeader
        icon={FolderOpen}
        eyebrow={ar ? "بيانات مباشرة" : "Live data"}
        title={ar ? "أحدث ملفات الطلاب" : "Recent student records"}
        action={
          <button type="button" onClick={onOpenAll}>
            {ar ? "عرض كل الطلاب" : "View all students"}
            <ArrowLeft size={16} aria-hidden="true" />
          </button>
        }
      />

      <div className="studentFilesTable" role="table" aria-label={ar ? "أحدث ملفات الطلاب" : "Recent student records"}>
        {records.map((record) => (
          <StudentFileCard
            key={record.id}
            record={record}
            thesisStatus={
              thesisLabels[record.thesis_status] ||
              (ar ? "لا توجد رسالة مسجلة" : "No registered thesis")
            }
            labels={{
              enrollments: ar ? "قيد أكاديمي" : "enrollments",
              source: ar ? "من قاعدة البيانات" : "Database record",
            }}
          />
        ))}
      </div>
    </section>
  );
}
