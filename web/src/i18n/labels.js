export const LABELS = {
  roles: {
    STAFF: { ar: "موظف تشغيل", en: "Staff Member" },
    PROGRAM_DIRECTOR: { ar: "مدير البرنامج", en: "Program Director" },
    DEAN: { ar: "العميد", en: "Dean" },
    VICE_DEAN: { ar: "وكيل الكلية", en: "Vice Dean" },
  },

  degrees: {
    MASTER: { ar: "ماجستير", en: "Master's Degree" },
    PHD: { ar: "دكتوراه", en: "PhD" },
    DIPLOMA: { ar: "دبلوم", en: "Diploma" },
  },

  statuses: {
    REGISTERED: { ar: "مسجلة", en: "Registered" },
    SUBMITTED: { ar: "تم التقديم", en: "Submitted" },
    APPROVED: { ar: "معتمد", en: "Approved" },
    FINAL_APPROVED: { ar: "اعتماد نهائي", en: "Final Approved" },
    DIRECTOR_APPROVED: { ar: "اعتماد مدير الدراسات العليا", en: "Director Approved" },
    PENDING: { ar: "قيد المراجعة", en: "Pending" },
    UNDER_REVIEW: { ar: "تحت المراجعة", en: "Under Review" },
    COMPLETED: { ar: "مكتملة", en: "Completed" },
    NO_THESIS: { ar: "بدون رسالة", en: "No Thesis" },
  },
};

export function label(type, value, language = "ar") {
  return LABELS[type]?.[value]?.[language] || value || "—";
}
