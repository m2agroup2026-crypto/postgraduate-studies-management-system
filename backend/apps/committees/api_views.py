from datetime import date
from math import ceil

from django.db import transaction
from django.db.models import Q
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.theses.models import Thesis

from .models import DefenseCommittee, DefenseScheduleEvent

VIEW_PERMISSION = "committees.view"
MANAGE_PERMISSION = "committees.manage"

LEGACY_VIEW_ROLES = {
    "DEAN",
    "VICE_DEAN",
    "VICE_DEAN_POSTGRADUATE",
    "VP_POSTGRADUATE_RESEARCH",
    "POSTGRADUATE_DIRECTOR",
    "PROGRAM_DIRECTOR",
    "STAFF",
    "REVIEWER",
    "SUPERVISOR",
}

LEGACY_MANAGE_ROLES = {
    "POSTGRADUATE_DIRECTOR",
    "PROGRAM_DIRECTOR",
    "STAFF",
}


def has_dynamic_permission(user, permission_codes):
    active_roles = user.roles.filter(is_active=True)
    if not active_roles.exists():
        return None
    return active_roles.filter(
        permissions__code__in=permission_codes,
        permissions__is_active=True,
    ).exists()


def can_view_committees(user):
    if user.is_superuser or user.is_staff:
        return True
    dynamic = has_dynamic_permission(user, {VIEW_PERMISSION, MANAGE_PERMISSION})
    if dynamic is not None:
        return dynamic
    return user.role in LEGACY_VIEW_ROLES


def can_manage_committees(user):
    if user.is_superuser or user.is_staff:
        return True
    dynamic = has_dynamic_permission(user, {MANAGE_PERMISSION})
    if dynamic is not None:
        return dynamic
    return user.role in LEGACY_MANAGE_ROLES


def parse_positive_int(raw_value, default, maximum=None):
    try:
        value = int(raw_value)
    except (TypeError, ValueError):
        value = default
    if value < 1:
        value = default
    if maximum is not None:
        value = min(value, maximum)
    return value


def parse_date(raw_value):
    if raw_value in (None, ""):
        return None
    try:
        return date.fromisoformat(str(raw_value))
    except ValueError as exc:
        raise ValueError("invalid_date") from exc


def serialize_department(department):
    faculty = department.faculty
    university = faculty.university if faculty else None
    return {
        "id": department.id,
        "code": department.code,
        "name_ar": department.name_ar,
        "name_en": department.name_en,
        "faculty": (
            {
                "id": faculty.id,
                "code": faculty.code,
                "name_ar": faculty.name_ar,
                "name_en": faculty.name_en,
            }
            if faculty
            else None
        ),
        "university": (
            {
                "id": university.id,
                "code": university.code,
                "name_ar": university.name_ar,
                "name_en": university.name_en,
            }
            if university
            else None
        ),
    }


def get_defense(thesis):
    try:
        return thesis.defensecommittee
    except DefenseCommittee.DoesNotExist:
        return None


def serialize_record(thesis):
    defense = get_defense(thesis)
    return {
        "thesis": {
            "id": thesis.id,
            "title_ar": thesis.title_ar,
            "status": thesis.status,
        },
        "student": {
            "id": thesis.student.id,
            "university_id": thesis.student.university_id,
            "name_ar": thesis.student.name_ar,
        },
        "department": serialize_department(thesis.student.department),
        "defense": (
            {
                "id": defense.id,
                "defense_date": defense.defense_date,
                "status": defense.status,
            }
            if defense
            else None
        ),
    }


def defense_queryset():
    return Thesis.objects.select_related(
        "student",
        "student__department",
        "student__department__faculty",
        "student__department__faculty__university",
        "defensecommittee",
    )


def serialize_history(defense):
    if not defense:
        return []
    events = defense.schedule_events.select_related("performed_by").all()
    return [
        {
            "id": item.id,
            "event_type": item.event_type,
            "old_date": item.old_date,
            "new_date": item.new_date,
            "notes": item.notes,
            "created_at": item.created_at,
            "performed_by": {
                "id": item.performed_by_id,
                "username": item.performed_by.username,
                "name": item.performed_by.effective_name,
                "role": item.performed_by.role,
            },
        }
        for item in events
    ]


def detail_payload(user, thesis):
    defense = get_defense(thesis)
    return {
        "record": serialize_record(thesis),
        "schedule_history": serialize_history(defense),
        "capabilities": {
            "can_view": True,
            "can_manage": can_manage_committees(user),
        },
    }


class CommitteeCollectionView(APIView):
    def get(self, request):
        if not can_view_committees(request.user):
            return Response({"error": "غير مصرح لك بعرض اللجان والمناقشات"}, status=403)

        queryset = defense_queryset()
        search = request.query_params.get("q", "").strip()
        department_id = request.query_params.get("department", "").strip()
        schedule_filter = request.query_params.get("schedule", "").strip().lower()
        date_from_raw = request.query_params.get("date_from", "").strip()
        date_to_raw = request.query_params.get("date_to", "").strip()

        if search:
            queryset = queryset.filter(
                Q(title_ar__icontains=search)
                | Q(student__name_ar__icontains=search)
                | Q(student__university_id__icontains=search)
                | Q(student__department__name_ar__icontains=search)
                | Q(student__department__name_en__icontains=search)
            )
        if department_id:
            queryset = queryset.filter(student__department_id=department_id)

        today = date.today()
        if schedule_filter == "scheduled":
            queryset = queryset.filter(defensecommittee__defense_date__isnull=False)
        elif schedule_filter == "unscheduled":
            queryset = queryset.filter(
                Q(defensecommittee__isnull=True) | Q(defensecommittee__defense_date__isnull=True)
            )
        elif schedule_filter == "upcoming":
            queryset = queryset.filter(defensecommittee__defense_date__gte=today)
        elif schedule_filter == "past":
            queryset = queryset.filter(defensecommittee__defense_date__lt=today)

        try:
            date_from = parse_date(date_from_raw)
            date_to = parse_date(date_to_raw)
        except ValueError:
            return Response({"error": "صيغة تاريخ البحث غير صحيحة"}, status=400)

        if date_from:
            queryset = queryset.filter(defensecommittee__defense_date__gte=date_from)
        if date_to:
            queryset = queryset.filter(defensecommittee__defense_date__lte=date_to)
        if date_from and date_to and date_from > date_to:
            return Response({"error": "تاريخ البداية يجب ألا يتجاوز تاريخ النهاية"}, status=400)

        ordering = request.query_params.get("ordering", "date")
        ordering_map = {
            "date": "defensecommittee__defense_date",
            "-date": "-defensecommittee__defense_date",
            "student": "student__name_ar",
            "-student": "-student__name_ar",
            "department": "student__department__name_ar",
            "-department": "-student__department__name_ar",
        }
        queryset = queryset.order_by(ordering_map.get(ordering, "defensecommittee__defense_date"), "id")

        page = parse_positive_int(request.query_params.get("page"), 1)
        page_size = parse_positive_int(request.query_params.get("page_size"), 20, 100)
        total = queryset.count()
        pages = max(1, ceil(total / page_size)) if total else 0
        if pages and page > pages:
            page = pages
        start = (page - 1) * page_size
        end = start + page_size

        department_options = list(
            Thesis.objects.values(
                "student__department_id",
                "student__department__code",
                "student__department__name_ar",
                "student__department__name_en",
            )
            .distinct()
            .order_by("student__department__name_ar")
        )
        all_theses = Thesis.objects.all()
        scheduled_count = all_theses.filter(defensecommittee__defense_date__isnull=False).count()
        upcoming_count = all_theses.filter(defensecommittee__defense_date__gte=today).count()

        return Response(
            {
                "results": [serialize_record(thesis) for thesis in queryset[start:end]],
                "pagination": {
                    "page": page,
                    "page_size": page_size,
                    "total": total,
                    "pages": pages,
                },
                "summary": {
                    "total_theses": all_theses.count(),
                    "scheduled": scheduled_count,
                    "upcoming": upcoming_count,
                    "unscheduled": all_theses.count() - scheduled_count,
                },
                "filters": {"departments": department_options},
                "capabilities": {
                    "can_view": True,
                    "can_manage": can_manage_committees(request.user),
                },
            }
        )


class CommitteeDetailView(APIView):
    def get(self, request, thesis_id):
        if not can_view_committees(request.user):
            return Response({"error": "غير مصرح لك بعرض اللجان والمناقشات"}, status=403)

        try:
            thesis = defense_queryset().get(pk=thesis_id)
        except Thesis.DoesNotExist:
            return Response({"error": "سجل الرسالة العلمية غير موجود"}, status=404)

        return Response(detail_payload(request.user, thesis))


class CommitteeScheduleView(APIView):
    def post(self, request, thesis_id):
        if not can_manage_committees(request.user):
            return Response({"error": "غير مصرح لك بإدارة جدول المناقشات"}, status=403)

        notes = str(request.data.get("notes", "")).strip()
        if len(notes) > 2000:
            return Response({"error": "ملاحظات الجدولة طويلة جدًا"}, status=400)

        try:
            new_date = parse_date(request.data.get("defense_date"))
        except ValueError:
            return Response({"error": "صيغة تاريخ المناقشة غير صحيحة"}, status=400)

        with transaction.atomic():
            try:
                thesis = Thesis.objects.select_for_update().get(pk=thesis_id)
            except Thesis.DoesNotExist:
                return Response({"error": "سجل الرسالة العلمية غير موجود"}, status=404)

            try:
                defense = DefenseCommittee.objects.select_for_update().get(thesis=thesis)
            except DefenseCommittee.DoesNotExist:
                defense = None

            if defense is None:
                if new_date is None:
                    return Response({"error": "لا توجد مناقشة مجدولة لإلغاء تاريخها"}, status=400)
                defense = DefenseCommittee.objects.create(thesis=thesis, defense_date=new_date)
                DefenseScheduleEvent.objects.create(
                    committee=defense,
                    event_type=DefenseScheduleEvent.EventType.SCHEDULED,
                    new_date=new_date,
                    performed_by=request.user,
                    notes=notes,
                )
            else:
                old_date = defense.defense_date
                if old_date == new_date:
                    refreshed = defense_queryset().get(pk=thesis.pk)
                    return Response(detail_payload(request.user, refreshed))

                defense.defense_date = new_date
                defense.save(update_fields=["defense_date"])
                event_type = (
                    DefenseScheduleEvent.EventType.DATE_CLEARED
                    if new_date is None
                    else DefenseScheduleEvent.EventType.RESCHEDULED
                    if old_date is not None
                    else DefenseScheduleEvent.EventType.SCHEDULED
                )
                DefenseScheduleEvent.objects.create(
                    committee=defense,
                    event_type=event_type,
                    old_date=old_date,
                    new_date=new_date,
                    performed_by=request.user,
                    notes=notes,
                )

        refreshed = defense_queryset().get(pk=thesis_id)
        return Response(detail_payload(request.user, refreshed))
