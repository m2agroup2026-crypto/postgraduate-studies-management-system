from datetime import date, timedelta

from django.core.exceptions import ValidationError
from django.db import transaction
from django.db.models import Count
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.academics.models import AcademicDegree, Program
from apps.committees.models import DefenseCommittee
from apps.core.authorization import effective_permissions, effective_roles, has_permission
from apps.students.models import Student
from apps.theses.models import Thesis

from .models import DashboardMetricCard, DashboardNavigationItem

ROLE_IDENTITIES = {
    "DEAN": {"name": "الأستاذ الدكتور علاء عطية", "title": "عميد كلية الطب"},
    "VICE_DEAN_POSTGRADUATE": {
        "name": "الأستاذ الدكتور محمد عبد الباسط خلاف",
        "title": "وكيل الكلية لشئون الدراسات العليا والبحوث",
    },
    "POSTGRADUATE_DIRECTOR": {
        "name": "مدير الدراسات العليا",
        "title": "مدير إدارة الدراسات العليا",
    },
    "PROGRAM_DIRECTOR": {
        "name": "مدير البرنامج",
        "title": "مدير برنامج الدراسات العليا",
    },
}

PENDING_STATUS_BY_ROLE = {
    "REVIEWER": ("SUBMITTED", "طلبات تنتظر المراجعة"),
    "POSTGRADUATE_DIRECTOR": ("UNDER_REVIEW", "طلبات تنتظر قرار مدير الدراسات العليا"),
    "VICE_DEAN_POSTGRADUATE": ("DIRECTOR_APPROVED", "طلبات تنتظر قرار الوكيل"),
    "DEAN": ("VICE_DEAN_APPROVED", "طلبات تنتظر قرار العميد"),
    "VP_POSTGRADUATE_RESEARCH": ("DEAN_APPROVED", "طلبات تنتظر الاعتماد النهائي"),
}


def can_manage_dashboard(user):
    return has_permission(user, "dashboard.manage")


def serialize_navigation(user, include_inactive=False, enforce_permissions=True):
    queryset = DashboardNavigationItem.objects.all()
    if not include_inactive:
        queryset = queryset.filter(is_active=True, is_operational=True)

    items = []
    for item in queryset:
        if (
            enforce_permissions
            and item.required_permission
            and not has_permission(user, item.required_permission)
        ):
            continue
        items.append(
            {
                "key": item.key,
                "label_ar": item.label_ar,
                "label_en": item.label_en,
                "route": item.route,
                "icon": item.icon,
                "required_permission": item.required_permission,
                "sort_order": item.sort_order,
                "is_active": item.is_active,
                "is_operational": item.is_operational,
            }
        )
    return items


def pending_metric(user):
    roles = effective_roles(user)
    for role in PENDING_STATUS_BY_ROLE:
        if role in roles:
            status, label = PENDING_STATUS_BY_ROLE[role]
            return {
                "value": Thesis.objects.filter(status=status).count(),
                "label_ar": label,
                "definition": f"thesis.status = {status}",
            }
    return {
        "value": 0,
        "label_ar": "طلبات تنتظر قرارك",
        "definition": "No workflow decision stage assigned",
    }


def dashboard_metrics(user):
    today = date.today()
    pending = pending_metric(user)
    values = {
        "students": Student.objects.count(),
        "theses": Thesis.objects.count(),
        "defenses": DefenseCommittee.objects.filter(defense_date__gte=today).count(),
        "pending": pending["value"],
    }
    definitions = {
        "students": "عدد سجلات الطلاب في قاعدة البيانات",
        "theses": "عدد الرسائل العلمية المسجلة",
        "defenses": "عدد المناقشات بتاريخ اليوم أو بعده",
        "pending": pending["definition"],
    }
    return values, definitions, pending


def recent_student_records(user, limit=6):
    if not has_permission(user, "students.view"):
        return []

    students = (
        Student.objects.select_related("department", "thesis")
        .annotate(enrollments_count=Count("academic_enrollments", distinct=True))
        .order_by("-id")[:limit]
    )
    records = []
    for student in students:
        try:
            thesis_status = student.thesis.status
        except Thesis.DoesNotExist:
            thesis_status = None
        records.append(
            {
                "id": student.id,
                "university_id": student.university_id,
                "name_ar": student.name_ar,
                "department": student.department.name_ar,
                "enrollments_count": student.enrollments_count,
                "thesis_status": thesis_status,
            }
        )
    return records


def serialize_metrics(user, include_inactive=False):
    queryset = DashboardMetricCard.objects.all()
    if not include_inactive:
        queryset = queryset.filter(is_active=True)
    pending = pending_metric(user)
    result = []
    for item in queryset:
        label_ar = pending["label_ar"] if item.key == "pending" else item.label_ar
        result.append(
            {
                "key": item.key,
                "label_ar": label_ar,
                "label_en": item.label_en,
                "icon": item.icon,
                "sort_order": item.sort_order,
                "is_active": item.is_active,
            }
        )
    return result


def assistant_actions(user, navigation):
    visible = {item["key"] for item in navigation}
    definitions = [
        ("students", "عرض الطلاب", "navigate", "students", "students.view"),
        ("theses", "عرض الرسائل العلمية", "navigate", "theses", "theses.view"),
        (
            "committees",
            "عرض اللجان والمناقشات",
            "navigate",
            "committees",
            "committees.view",
        ),
        (
            "pending",
            "ما الطلبات التي تنتظر قراري؟",
            "message",
            "ما الطلبات التي تنتظر قراري؟",
            None,
        ),
    ]
    workflow_role = bool(effective_roles(user).intersection(PENDING_STATUS_BY_ROLE))
    return [
        {"id": key, "label": label, "type": kind, "target": target}
        for key, label, kind, target, permission in definitions
        if (kind != "navigate" or target in visible)
        and (not permission or has_permission(user, permission))
        and (key != "pending" or workflow_role)
    ]


def apply_configuration(item, payload, allowed_fields):
    for field in allowed_fields:
        if field in payload:
            setattr(item, field, payload[field])
    item.full_clean()
    item.save()


class MeView(APIView):
    def get(self, request):
        roles = effective_roles(request.user)
        identity_role = next(
            (role for role in ROLE_IDENTITIES if role in roles),
            request.user.role,
        )
        identity = ROLE_IDENTITIES.get(identity_role, {})
        return Response(
            {
                "username": request.user.username,
                "role": request.user.role,
                "roles": sorted(roles),
                "permissions": sorted(effective_permissions(request.user)),
                "name": request.user.effective_name
                if request.user.display_name_ar
                else identity.get("name"),
                "title": request.user.job_title_ar or identity.get("title"),
                "language": request.user.preferred_language or "ar",
                "can_manage_dashboard": can_manage_dashboard(request.user),
            }
        )


class DashboardView(APIView):
    def get(self, request):
        roles = effective_roles(request.user)
        identity_role = next(
            (role for role in ROLE_IDENTITIES if role in roles),
            request.user.role,
        )
        identity = ROLE_IDENTITIES.get(identity_role, ROLE_IDENTITIES["PROGRAM_DIRECTOR"])
        navigation = serialize_navigation(request.user)
        metrics, metric_definitions, pending = dashboard_metrics(request.user)
        today = date.today()
        upcoming_limit = today + timedelta(days=30)
        upcoming_30_days = DefenseCommittee.objects.filter(
            defense_date__range=(today, upcoming_limit)
        ).count()

        departments = list(
            Student.objects.values("department__name_ar")
            .annotate(total=Count("id"))
            .order_by("-total")[:6]
        )
        degrees = list(
            AcademicDegree.objects.values("code", "name_ar", "level").annotate(
                programs_count=Count("programs")
            )
        )
        programs = list(
            Program.objects.values(
                "code",
                "name_ar",
                "department__name_ar",
                "degree__name_ar",
            )
        )

        alerts = []
        if pending["value"]:
            alerts.append(
                {
                    "level": "warning",
                    "text": f"{pending['value']} طلبات تنتظر قرارك في المرحلة الحالية",
                }
            )
        if upcoming_30_days:
            alerts.append(
                {
                    "level": "info",
                    "text": f"{upcoming_30_days} مناقشات مقررة خلال الثلاثين يومًا القادمة",
                }
            )

        return Response(
            {
                "identity": identity,
                "role": request.user.role,
                "roles": sorted(roles),
                "metrics": metrics,
                "metric_definitions": metric_definitions,
                "ui": {
                    "navigation": navigation,
                    "metrics": serialize_metrics(request.user),
                },
                "assistant": {"quick_actions": assistant_actions(request.user, navigation)},
                "recent_students": recent_student_records(request.user),
                "departments": departments,
                "academic_structure": {"degrees": degrees, "programs": programs},
                "alerts": alerts,
            }
        )


class DashboardConfigurationView(APIView):
    def get(self, request):
        if not can_manage_dashboard(request.user):
            return Response({"error": "غير مصرح لك بإدارة إعدادات لوحة التحكم"}, status=403)
        return Response(
            {
                "navigation": serialize_navigation(
                    request.user,
                    include_inactive=True,
                    enforce_permissions=False,
                ),
                "metrics": serialize_metrics(request.user, include_inactive=True),
            }
        )

    @transaction.atomic
    def patch(self, request):
        if not can_manage_dashboard(request.user):
            return Response({"error": "غير مصرح لك بإدارة إعدادات لوحة التحكم"}, status=403)

        navigation = request.data.get("navigation", [])
        metrics = request.data.get("metrics", [])
        if not isinstance(navigation, list) or not isinstance(metrics, list):
            return Response({"error": "صيغة إعدادات لوحة التحكم غير صحيحة"}, status=400)

        nav_fields = {
            "label_ar",
            "label_en",
            "route",
            "icon",
            "required_permission",
            "sort_order",
            "is_active",
        }
        metric_fields = {
            "label_ar",
            "label_en",
            "icon",
            "sort_order",
            "is_active",
        }

        try:
            for payload in navigation:
                key = payload.get("key")
                if not key:
                    return Response({"error": "كل عنصر قائمة يجب أن يحتوي على key"}, status=400)
                try:
                    item = DashboardNavigationItem.objects.get(key=key)
                except DashboardNavigationItem.DoesNotExist:
                    return Response({"error": f"عنصر القائمة غير معروف: {key}"}, status=400)
                apply_configuration(item, payload, nav_fields)

            for payload in metrics:
                key = payload.get("key")
                if not key:
                    return Response({"error": "كل بطاقة مؤشر يجب أن تحتوي على key"}, status=400)
                try:
                    item = DashboardMetricCard.objects.get(key=key)
                except DashboardMetricCard.DoesNotExist:
                    return Response({"error": f"بطاقة المؤشر غير معروفة: {key}"}, status=400)
                apply_configuration(item, payload, metric_fields)
        except ValidationError as exc:
            transaction.set_rollback(True)
            return Response(
                {"error": "بعض القيم غير صالحة", "details": exc.message_dict},
                status=400,
            )

        return Response(
            {
                "navigation": serialize_navigation(
                    request.user,
                    include_inactive=True,
                    enforce_permissions=False,
                ),
                "metrics": serialize_metrics(request.user, include_inactive=True),
            }
        )


class AssistantView(APIView):
    def post(self, request):
        question = str(request.data.get("message", "")).strip()
        if not question:
            return Response({"error": "اكتب سؤالك أولًا"}, status=400)

        normalized = question.lower()
        if "طالب" in normalized or "student" in normalized:
            if not has_permission(request.user, "students.view"):
                return Response({"error": "غير مصرح لك بعرض بيانات الطلاب"}, status=403)
            answer = f"إجمالي الطلاب المسجلين في النظام {Student.objects.count()}."
        elif "مناقش" in normalized or "لجان" in normalized or "defense" in normalized:
            if not has_permission(request.user, "committees.view"):
                return Response({"error": "غير مصرح لك بعرض بيانات اللجان"}, status=403)
            answer = (
                "إجمالي المناقشات القادمة "
                f"{DefenseCommittee.objects.filter(defense_date__gte=date.today()).count()}."
            )
        elif "رسائل" in normalized or "thes" in normalized:
            if not has_permission(request.user, "theses.view"):
                return Response({"error": "غير مصرح لك بعرض الرسائل العلمية"}, status=403)
            answer = f"إجمالي الرسائل العلمية المسجلة {Thesis.objects.count()}."
        elif "قرار" in normalized or "متابعة" in normalized or "pending" in normalized:
            pending = pending_metric(request.user)
            answer = f"{pending['label_ar']}: {pending['value']}."
        else:
            allowed = []
            if has_permission(request.user, "students.view"):
                allowed.append("الطلاب")
            if has_permission(request.user, "theses.view"):
                allowed.append("الرسائل العلمية")
            if has_permission(request.user, "committees.view"):
                allowed.append("اللجان والمناقشات")
            answer = "يمكنني مساعدتك في " + " و".join(allowed) + "."

        return Response(
            {
                "answer": answer,
                "role": request.user.role,
                "requires_confirmation": False,
                "source": "authorized_system_data",
            }
        )
