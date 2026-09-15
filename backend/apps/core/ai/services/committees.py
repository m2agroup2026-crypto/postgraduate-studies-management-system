from datetime import date, timedelta

from django.db.models import Count

from apps.committees.models import DefenseCommittee
from apps.core.authorization import has_permission

from . import denied, response, status_label


def handle(question, user, language):
    if not has_permission(user, "committees.view"):
        return denied("committees", language)

    text = question.lower()
    if "upcoming" in text or "قادمة" in text or "القادمة" in text:
        end = date.today() + timedelta(days=30)
        queryset = DefenseCommittee.objects.filter(defense_date__range=(date.today(), end))
        count = queryset.count()
        answer = (
            f"المناقشات المقررة خلال 30 يومًا: {count}."
            if language == "ar"
            else f"Defenses scheduled in the next 30 days: {count}."
        )
        return response("committees", answer, {"count": count, "window_days": 30})

    if "status" in text or "حالة" in text or "distribution" in text:
        rows = list(
            DefenseCommittee.objects.values("status").annotate(count=Count("id")).order_by("status")
        )
        lines = [f"{status_label(row['status'], language)}: {row['count']}" for row in rows]
        heading = "حالة لجان المناقشة" if language == "ar" else "Defense committee status"
        return response(
            "committees", f"{heading}\n" + ("\n".join(lines) or "—"), {"distribution": rows}
        )

    scheduled = DefenseCommittee.objects.exclude(defense_date__isnull=True).count()
    answer = (
        f"لجان المناقشة المجدولة: {scheduled}."
        if language == "ar"
        else f"Scheduled defense committees: {scheduled}."
    )
    return response("committees", answer, {"scheduled": scheduled})
