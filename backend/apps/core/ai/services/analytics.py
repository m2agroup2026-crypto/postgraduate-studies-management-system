from django.db.models import Count

from apps.core.authorization import has_permission
from apps.students.models import Student
from apps.theses.models import Thesis

from . import denied, response


def handle(question, user, language):
    if not has_permission(user, "reports.view"):
        return denied("analytics", language)

    departments = list(
        Student.objects.values("department__name_ar", "department__name_en")
        .annotate(students=Count("id"))
        .order_by("-students")[:10]
    )
    students = Student.objects.count()
    theses = Thesis.objects.count()
    completed = Thesis.objects.filter(status="COMPLETED").count()
    completion_rate = round((completed / theses) * 100, 1) if theses else 0
    if language == "ar":
        answer = (
            f"الملخص التنفيذي\nالطلاب: {students}\nالرسائل: {theses}\n"
            f"الرسائل المكتملة: {completed}\nنسبة الاكتمال: {completion_rate}%"
        )
    else:
        answer = (
            f"Executive summary\nStudents: {students}\nTheses: {theses}\n"
            f"Completed theses: {completed}\nCompletion rate: {completion_rate}%"
        )
    return response(
        "analytics",
        answer,
        {
            "students": students,
            "theses": theses,
            "completed": completed,
            "completion_rate": completion_rate,
            "departments": departments,
        },
    )
