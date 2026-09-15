from django.db.models import Count

from apps.core.authorization import effective_roles, has_permission
from apps.theses.models import Thesis

from . import denied, response, status_label

ROLE_STAGE = {
    "REVIEWER": "SUBMITTED",
    "POSTGRADUATE_DIRECTOR": "UNDER_REVIEW",
    "VICE_DEAN_POSTGRADUATE": "DIRECTOR_APPROVED",
    "DEAN": "VICE_DEAN_APPROVED",
    "VP_POSTGRADUATE_RESEARCH": "DEAN_APPROVED",
}

ACTIVE_STATUSES = tuple(ROLE_STAGE.values())


def handle(question, user, language):
    if not has_permission(user, "theses.view"):
        return denied("workflow", language)

    roles = effective_roles(user)
    personal_stage = next((ROLE_STAGE[role] for role in ROLE_STAGE if role in roles), None)
    text = question.lower()
    if ("my" in text or "قراري" in text or "قرار" in text) and personal_stage:
        count = Thesis.objects.filter(status=personal_stage).count()
        label = status_label(personal_stage, language)
        answer = (
            f"طلبات تنتظر إجراءك في مرحلة {label}: {count}."
            if language == "ar"
            else f"Items awaiting your action at {label}: {count}."
        )
        return response("workflow", answer, {"status": personal_stage, "count": count})

    rows = list(
        Thesis.objects.filter(status__in=ACTIVE_STATUSES)
        .values("status")
        .annotate(count=Count("id"))
        .order_by("-count")
    )
    total = sum(row["count"] for row in rows)
    bottleneck = rows[0] if rows else None
    if bottleneck:
        label = status_label(bottleneck["status"], language)
        answer = (
            f"إجمالي العناصر النشطة في مسار الاعتماد: {total}. "
            f"أكبر نقطة تراكم: {label} بعدد {bottleneck['count']}."
            if language == "ar"
            else (
                f"Active approval items: {total}. Largest queue: {label} "
                f"with {bottleneck['count']} items."
            )
        )
    else:
        answer = (
            "لا توجد عناصر معلقة في مسار الاعتماد."
            if language == "ar"
            else "No items are pending in the approval workflow."
        )
    return response(
        "workflow", answer, {"count": total, "distribution": rows, "bottleneck": bottleneck}
    )
