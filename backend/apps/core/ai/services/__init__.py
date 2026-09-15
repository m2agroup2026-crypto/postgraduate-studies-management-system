"""Permission-scoped academic intelligence services."""

import re


def language_for(question):
    return "ar" if re.search(r"[\u0600-\u06ff]", question or "") else "en"


def response(intent, answer, data=None):
    return {"intent": intent, "answer": answer, "data": data or {}}


def denied(intent, language):
    answer = (
        "لا يملك حسابك صلاحية الوصول إلى هذه البيانات."
        if language == "ar"
        else "Your account is not permitted to access this data."
    )
    return response(intent, answer, {"authorized": False})


STATUS_LABELS = {
    "REGISTERED": ("مسجلة", "Registered"),
    "SUBMITTED": ("مقدمة للمراجعة", "Submitted for review"),
    "UNDER_REVIEW": ("قيد المراجعة", "Under review"),
    "DIRECTOR_APPROVED": ("معتمدة من مدير البرنامج", "Director approved"),
    "VICE_DEAN_APPROVED": ("معتمدة من وكيل الكلية", "Vice dean approved"),
    "DEAN_APPROVED": ("معتمدة من العميد", "Dean approved"),
    "FINAL_APPROVED": ("معتمدة نهائيًا", "Final approved"),
    "APPROVED": ("معتمدة", "Approved"),
    "COMPLETED": ("مكتملة", "Completed"),
    "PENDING": ("قيد الانتظار", "Pending"),
    "SCHEDULED": ("مجدولة", "Scheduled"),
}


def status_label(status, language):
    labels = STATUS_LABELS.get(status, (status or "—", status or "—"))
    return labels[0 if language == "ar" else 1]
