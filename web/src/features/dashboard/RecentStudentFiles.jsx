import React from "react";
import Panel from "../../components/ui/Panel";
import { ArrowLeft, FolderOpen } from "lucide-react";
import SectionHeader from "../../components/ui/SectionHeader";
import StudentFileCard from "../../components/ui/StudentFileCard";

const thesisLabels = {
  REGISTERED: { ar: "مسجلة", en: "Registered" },
  SUBMITTED: { ar: "مقدمة للمراجعة", en: "Submitted for review" },
  UNDER_REVIEW: { ar: "قيد المراجعة", en: "Under review" },
  DIRECTOR_APPROVED: { ar: "بانتظار قرار الوكيل", en: "Awaiting vice dean decision" },
  VICE_DEAN_APPROVED: { ar: "معتمدة من الوكيل", en: "Approved by vice dean" },
  DEAN_APPROVED: { ar: "معتمدة من العميد", en: "Approved by dean" },
  FINAL_APPROVED: { ar: "معتمدة نهائيًا", en: "Final approved" },
  RETURNED: { ar: "معادة للاستكمال", en: "Returned for completion" },
  REJECTED: { ar: "مرفوضة", en: "Rejected" },
  COMPLETED: { ar: "مكتملة", en: "Completed" },
};

export default function RecentStudentFiles({ records, language, onOpenAll }) {
  const ar = language === "ar";

  if (!records.length) return null;

  return (
    <Panel className="studentFilesPanel" aria-labelledby="recent-student-files">
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
              thesisLabels[record.thesis_status]
                ? thesisLabels[record.thesis_status][ar ? "ar" : "en"]
                : (ar ? "لا توجد رسالة مسجلة" : "No registered thesis")
            }
            labels={{
              enrollments: ar ? "قيد أكاديمي" : "enrollments",
              source: ar ? "من قاعدة البيانات" : "Database record",
            }}
          />
        ))}
      </div>
    </Panel>
  );
}
