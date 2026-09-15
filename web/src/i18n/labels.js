export const EMPTY_VALUE = "—";

const LABELS = {
  statuses: {
    REGISTERED: { ar: "مسجل", en: "Registered" },
    DRAFT: { ar: "مسودة", en: "Draft" },
    SUBMITTED: { ar: "مقدم للمراجعة", en: "Submitted" },
    APPROVED: { ar: "معتمد", en: "Approved" },
    FINAL_APPROVED: { ar: "معتمد نهائيًا", en: "Final approved" },
    DIRECTOR_APPROVED: { ar: "معتمد من مدير البرنامج", en: "Director approved" },
    VICE_DEAN_APPROVED: { ar: "معتمد من وكيل الكلية", en: "Vice Dean approved" },
    DEAN_APPROVED: { ar: "معتمد من عميد الكلية", en: "Dean approved" },
    UNDER_REVIEW: { ar: "قيد المراجعة", en: "Under review" },
    COMPLETED: { ar: "مكتمل", en: "Completed" },
    PENDING: { ar: "قيد الانتظار", en: "Pending" },
    NO_THESIS: { ar: "بدون رسالة", en: "No thesis" },
    RETURNED: { ar: "معاد للاستكمال", en: "Returned" },
    REJECTED: { ar: "مرفوض", en: "Rejected" },
    SCHEDULED: { ar: "مجدول", en: "Scheduled" },
    RESCHEDULED: { ar: "أعيدت جدولته", en: "Rescheduled" },
    DATE_CLEARED: { ar: "أُلغي الموعد", en: "Date cleared" },
  },
  degrees: {
    MASTER: { ar: "ماجستير", en: "Master's" },
    PHD: { ar: "دكتوراه", en: "PhD" },
    DIPLOMA: { ar: "دبلوم", en: "Diploma" },
  },
  roles: {
    STAFF: { ar: "موظف دراسات عليا", en: "Postgraduate staff" },
    PROGRAM_DIRECTOR: { ar: "مدير البرنامج", en: "Program Director" },
    DEAN: { ar: "عميد الكلية", en: "Dean" },
    VICE_DEAN_POSTGRADUATE: { ar: "وكيل الكلية للدراسات العليا والبحوث", en: "Vice Dean for Postgraduate Studies and Research" },
    PLATFORM_ADMIN: { ar: "مدير المنصة", en: "Platform Administrator" },
  },
  actions: {
    SUBMIT: { ar: "تقديم", en: "Submit" },
    REVIEW: { ar: "بدء المراجعة", en: "Start review" },
    DIRECTOR_APPROVE: { ar: "اعتماد مدير البرنامج", en: "Director approval" },
    VICE_DEAN_APPROVE: { ar: "اعتماد وكيل الكلية", en: "Vice Dean approval" },
    DEAN_APPROVE: { ar: "اعتماد العميد", en: "Dean approval" },
    FINAL_APPROVE: { ar: "الاعتماد النهائي", en: "Final approval" },
    REJECT: { ar: "رفض", en: "Reject" },
    RETURN: { ar: "إعادة للاستكمال", en: "Return for completion" },
    SCHEDULED: { ar: "تمت الجدولة", en: "Scheduled" },
    RESCHEDULED: { ar: "إعادة جدولة", en: "Rescheduled" },
    DATE_CLEARED: { ar: "إلغاء التاريخ", en: "Date cleared" },
  },
};

export function displayValue(value, fallback = EMPTY_VALUE) {
  return value === null || value === undefined || value === "" ? fallback : value;
}

export function localizedField(record, field, language = "ar", fallback = EMPTY_VALUE) {
  if (!record) return fallback;
  const primary = language === "en" ? record[`${field}_en`] : record[`${field}_ar`];
  const secondary = language === "en" ? record[`${field}_ar`] : record[`${field}_en`];
  return displayValue(primary || secondary || record[field], fallback);
}

export function localizedName(value, language = "ar", fallback = EMPTY_VALUE) {
  return typeof value === "object" && value !== null
    ? localizedField(value, "name", language, fallback)
    : displayValue(value, fallback);
}

export function localizedLabel(group, value, language = "ar", fallback = EMPTY_VALUE) {
  if (!value) return fallback;
  if (typeof value === "object") return localizedName(value, language, fallback);
  const label = LABELS[group]?.[value];
  return label?.[language] || label?.ar || displayValue(value, fallback);
}

export const statusLabel = (value, language) => localizedLabel("statuses", value, language);
export const degreeLabel = (value, language) => localizedLabel("degrees", value, language);
export const roleLabel = (value, language) => localizedLabel("roles", value, language);
export const actionLabel = (value, language) => localizedLabel("actions", value, language);

export function statusTone(status) {
  if (["APPROVED", "FINAL_APPROVED", "DEAN_APPROVED", "VICE_DEAN_APPROVED", "DIRECTOR_APPROVED", "COMPLETED"].includes(status)) return "success";
  if (status === "REJECTED") return "danger";
  if (["RETURNED", "SUBMITTED", "UNDER_REVIEW", "PENDING"].includes(status)) return "warning";
  return "info";
}
