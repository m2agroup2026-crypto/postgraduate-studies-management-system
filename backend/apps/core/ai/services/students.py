import re

from django.db.models import Q

from apps.core.authorization import has_permission
from apps.students.models import Student

from . import denied, response, status_label


def _search_term(question):
    quoted = re.search(r"['\"]([^'\"]+)['\"]", question)
    if quoted:
        return quoted.group(1).strip()
    identifier = re.search(r"\b[A-Z][A-Z0-9]*[-/][A-Z0-9-]+\b", question, re.IGNORECASE)
    return identifier.group(0).strip() if identifier else ""


def handle(question, user, language):
    if not has_permission(user, "students.view"):
        return denied("students", language)

    term = _search_term(question)
    if not term:
        total = Student.objects.count()
        answer = (
            f"إجمالي طلاب الدراسات العليا المسجلين: {total}. اذكر الرقم الجامعي لعرض ملف محدد."
            if language == "ar"
            else (
                f"Total registered postgraduate students: {total}. "
                "Provide a university ID to open a specific profile."
            )
        )
        return response("students", answer, {"total": total})

    student = (
        Student.objects.select_related("department", "thesis")
        .filter(Q(university_id__iexact=term) | Q(name_ar__icontains=term))
        .first()
    )
    if not student:
        answer = (
            f"لم يتم العثور على طالب مطابق لـ {term}."
            if language == "ar"
            else f"No student matched {term}."
        )
        return response("students", answer, {"query": term, "found": False})

    thesis = getattr(student, "thesis", None)
    department = student.department.name_ar if student.department else "—"
    thesis_title = thesis.title_ar if thesis else "—"
    thesis_status = (
        status_label(thesis.status, language)
        if thesis
        else ("لا توجد رسالة" if language == "ar" else "No thesis")
    )
    if language == "ar":
        answer = (
            f"الطالب: {student.name_ar}\nالرقم الجامعي: {student.university_id}\n"
            f"القسم: {department}\nالرسالة: {thesis_title}\nحالة الرسالة: {thesis_status}"
        )
    else:
        department = student.department.name_en or department
        answer = (
            f"Student: {student.name_ar}\nUniversity ID: {student.university_id}\n"
            f"Department: {department}\nThesis: {thesis_title}\nThesis status: {thesis_status}"
        )
    return response(
        "students",
        answer,
        {"student_id": student.id, "university_id": student.university_id, "found": True},
    )
