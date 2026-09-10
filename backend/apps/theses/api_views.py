from math import ceil

from django.db.models import Q
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.committees.models import DefenseCommittee
from apps.core.authorization import has_permission
from apps.core.models import ApprovalAction
from apps.core.services.workflow import get_user_roles, transition
from apps.core.workflow.policy_checker import can_perform_action
from apps.core.workflow.rules import WORKFLOW_TRANSITIONS

from .models import Thesis

VIEW_PERMISSION = "theses.view"


def can_view_theses(user):
    return has_permission(user, VIEW_PERMISSION)


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


def serialize_thesis(thesis):
    defense = get_defense(thesis)
    return {
        "id": thesis.id,
        "title_ar": thesis.title_ar,
        "status": thesis.status,
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


def thesis_queryset():
    return Thesis.objects.select_related(
        "student",
        "student__department",
        "student__department__faculty",
        "student__department__faculty__university",
        "defensecommittee",
    )


def available_actions(user, thesis):
    roles = get_user_roles(user)
    return [
        action
        for action in WORKFLOW_TRANSITIONS.get(thesis.status, {})
        if can_perform_action(
            roles,
            "THESIS",
            action,
            current_status=thesis.status,
        )
    ]


def serialize_history(thesis):
    actions = ApprovalAction.objects.filter(
        request_type="Thesis",
        object_id=thesis.id,
    ).select_related("performed_by")
    return [
        {
            "id": item.id,
            "action": item.action,
            "from_status": item.from_status,
            "to_status": item.to_status,
            "notes": item.notes,
            "created_at": item.created_at,
            "performed_by": {
                "id": item.performed_by_id,
                "username": item.performed_by.username,
                "name": item.performed_by.effective_name,
                "role": item.performed_by.role,
            },
        }
        for item in actions
    ]


def detail_payload(user, thesis):
    return {
        "thesis": serialize_thesis(thesis),
        "workflow": {
            "history": serialize_history(thesis),
            "available_actions": available_actions(user, thesis),
        },
        "capabilities": {"can_view": True},
    }


class ThesisCollectionView(APIView):
    def get(self, request):
        if not can_view_theses(request.user):
            return Response({"error": "غير مصرح لك بعرض الرسائل العلمية"}, status=403)

        queryset = thesis_queryset()
        search = request.query_params.get("q", "").strip()
        department_id = request.query_params.get("department", "").strip()
        status_filter = request.query_params.get("status", "").strip()
        defense_filter = request.query_params.get("defense", "").strip().lower()

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
        if status_filter:
            queryset = queryset.filter(status=status_filter)
        if defense_filter == "scheduled":
            queryset = queryset.filter(defensecommittee__isnull=False)
        elif defense_filter == "unscheduled":
            queryset = queryset.filter(defensecommittee__isnull=True)

        ordering = request.query_params.get("ordering", "student")
        ordering_map = {
            "student": "student__name_ar",
            "-student": "-student__name_ar",
            "title": "title_ar",
            "-title": "-title_ar",
            "status": "status",
            "-status": "-status",
            "department": "student__department__name_ar",
            "-department": "-student__department__name_ar",
        }
        queryset = queryset.order_by(ordering_map.get(ordering, "student__name_ar"), "id")

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
        statuses = list(
            Thesis.objects.values_list("status", flat=True).distinct().order_by("status")
        )

        return Response(
            {
                "results": [serialize_thesis(thesis) for thesis in queryset[start:end]],
                "pagination": {
                    "page": page,
                    "page_size": page_size,
                    "total": total,
                    "pages": pages,
                },
                "filters": {
                    "departments": department_options,
                    "statuses": statuses,
                },
                "capabilities": {"can_view": True},
            }
        )


class ThesisDetailView(APIView):
    def get(self, request, thesis_id):
        if not can_view_theses(request.user):
            return Response({"error": "غير مصرح لك بعرض الرسائل العلمية"}, status=403)

        try:
            thesis = thesis_queryset().get(pk=thesis_id)
        except Thesis.DoesNotExist:
            return Response({"error": "سجل الرسالة العلمية غير موجود"}, status=404)

        return Response(detail_payload(request.user, thesis))


class ThesisActionView(APIView):
    def post(self, request, thesis_id):
        if not can_view_theses(request.user):
            return Response({"error": "غير مصرح لك بعرض الرسائل العلمية"}, status=403)

        try:
            thesis = thesis_queryset().get(pk=thesis_id)
        except Thesis.DoesNotExist:
            return Response({"error": "سجل الرسالة العلمية غير موجود"}, status=404)

        action = str(request.data.get("action", "")).strip().upper()
        notes = str(request.data.get("notes", "")).strip()
        if not action:
            return Response({"error": "يجب تحديد إجراء سير العمل"}, status=400)
        if len(notes) > 5000:
            return Response({"error": "ملاحظات الإجراء طويلة جدًا"}, status=400)

        try:
            updated = transition(thesis, action, request.user, notes=notes)
        except PermissionError:
            return Response({"error": "غير مصرح لك بتنفيذ هذا الإجراء"}, status=403)
        except ValueError:
            return Response({"error": "هذا الانتقال غير متاح من الحالة الحالية"}, status=400)

        refreshed = thesis_queryset().get(pk=updated.pk)
        return Response(detail_payload(request.user, refreshed))
