from django.db.models import Count

from apps.core.authorization import has_permission
from apps.theses.models import Thesis

from . import denied, response, status_label


def handle(question, user, language):
    if not has_permission(user, "theses.view"):
        return denied("theses", language)

    text = question.lower()
    if "distribution" in text or "توزيع" in text or "حسب الحالة" in text:
        rows = list(Thesis.objects.values("status").annotate(count=Count("id")).order_by("status"))
        lines = [f"{status_label(row['status'], language)}: {row['count']}" for row in rows]
        heading = "توزيع الرسائل حسب الحالة" if language == "ar" else "Thesis status distribution"
        return response(
            "theses", f"{heading}\n" + ("\n".join(lines) or "—"), {"distribution": rows}
        )

    if "completed" in text or "مكتمل" in text or "مكتملة" in text:
        count = Thesis.objects.filter(status="COMPLETED").count()
        answer = (
            f"عدد الرسائل المكتملة: {count}." if language == "ar" else f"Completed theses: {count}."
        )
        return response("theses", answer, {"status": "COMPLETED", "count": count})

    pending_statuses = [
        "SUBMITTED",
        "UNDER_REVIEW",
        "DIRECTOR_APPROVED",
        "VICE_DEAN_APPROVED",
        "DEAN_APPROVED",
    ]
    if "pending" in text or "تنتظر" in text or "قيد" in text:
        rows = list(
            Thesis.objects.filter(status__in=pending_statuses)
            .values("status")
            .annotate(count=Count("id"))
            .order_by("status")
        )
        total = sum(row["count"] for row in rows)
        answer = (
            f"إجمالي الرسائل في مراحل الانتظار والمراجعة: {total}."
            if language == "ar"
            else f"Theses in pending and review stages: {total}."
        )
        return response("theses", answer, {"count": total, "distribution": rows})

    total = Thesis.objects.count()
    answer = (
        f"إجمالي الرسائل العلمية المسجلة: {total}."
        if language == "ar"
        else f"Total registered theses: {total}."
    )
    return response("theses", answer, {"total": total})
