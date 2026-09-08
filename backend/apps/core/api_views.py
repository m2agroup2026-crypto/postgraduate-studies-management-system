from django.db import transaction
from django.db.models import Count
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.committees.models import DefenseCommittee
from apps.students.models import Student
from apps.theses.models import Thesis

from .models import DashboardMetricCard, DashboardNavigationItem

ROLE_IDENTITIES = {
    "DEAN": {"name": "الأستاذ الدكتور علاء عطية", "title": "عميد كلية الطب"},
    "VICE_DEAN": {"name": "الأستاذ الدكتور محمد عبد الباسط خلاف", "title": "وكيل الكلية لشؤون الدراسات العليا والبحوث"},
    "VICE_DEAN_POSTGRADUATE": {"name": "الأستاذ الدكتور محمد عبد الباسط خلاف", "title": "وكيل الكلية لشؤون الدراسات العليا والبحوث"},
    "POSTGRADUATE_DIRECTOR": {"name": "مدير الدراسات العليا", "title": "مدير إدارة الدراسات العليا"},
    "PROGRAM_DIRECTOR": {"name": "مدير البرنامج", "title": "مدير برنامج الدراسات العليا"},
}

DASHBOARD_MANAGER_ROLES = {
    "DEAN",
    "VICE_DEAN",
    "VICE_DEAN_POSTGRADUATE",
    "POSTGRADUATE_DIRECTOR",
}


def can_manage_dashboard(user):
    return bool(user.is_superuser or user.is_staff or user.role in DASHBOARD_MANAGER_ROLES)


def serialize_navigation(user, include_inactive=False):
    queryset = DashboardNavigationItem.objects.all()
    if not include_inactive:
        queryset = queryset.filter(is_active=True)

    items = []
    for item in queryset:
        if item.required_permission and not user.has_permission(item.required_permission):
            continue
        items.append({
            "key": item.key,
            "label_ar": item.label_ar,
            "label_en": item.label_en,
            "route": item.route,
            "icon": item.icon,
            "required_permission": item.required_permission,
            "sort_order": item.sort_order,
            "is_active": item.is_active,
        })
    return items


def serialize_metrics(include_inactive=False):
    queryset = DashboardMetricCard.objects.all()
    if not include_inactive:
        queryset = queryset.filter(is_active=True)
    return [
        {
            "key": item.key,
            "label_ar": item.label_ar,
            "label_en": item.label_en,
            "icon": item.icon,
            "sort_order": item.sort_order,
            "is_active": item.is_active,
        }
        for item in queryset
    ]


class MeView(APIView):
    def get(self, request):
        identity = ROLE_IDENTITIES.get(request.user.role, {})
        return Response({
            "username": request.user.username,
            "role": request.user.role,
            "name": request.user.effective_name if request.user.display_name_ar else identity.get("name"),
            "title": request.user.job_title_ar or identity.get("title"),
            "language": request.user.preferred_language or "ar",
            "can_manage_dashboard": can_manage_dashboard(request.user),
        })


class DashboardView(APIView):
    def get(self, request):
        identity = ROLE_IDENTITIES.get(request.user.role, ROLE_IDENTITIES["PROGRAM_DIRECTOR"])
        departments = list(
            Student.objects.values("department__name_ar")
            .annotate(total=Count("id"))
            .order_by("-total")[:6]
        )
        return Response({
            "identity": identity,
            "role": request.user.role,
            "metrics": {
                "students": Student.objects.count(),
                "theses": Thesis.objects.count(),
                "defenses": DefenseCommittee.objects.count(),
                "pending": Thesis.objects.exclude(status="COMPLETED").count(),
            },
            "ui": {
                "navigation": serialize_navigation(request.user),
                "metrics": serialize_metrics(),
            },
            "departments": departments,
            "alerts": [
                {"level": "warning", "text": "ملفات تحتاج مراجعة قبل اجتماع اللجنة القادم"},
                {"level": "info", "text": "مناقشات مقررة خلال الثلاثين يومًا القادمة"},
            ],
        })


class DashboardConfigurationView(APIView):
    def get(self, request):
        if not can_manage_dashboard(request.user):
            return Response({"error": "غير مصرح لك بإدارة إعدادات لوحة التحكم"}, status=403)
        return Response({
            "navigation": serialize_navigation(request.user, include_inactive=True),
            "metrics": serialize_metrics(include_inactive=True),
        })

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
        metric_fields = {"label_ar", "label_en", "icon", "sort_order", "is_active"}

        for payload in navigation:
            key = payload.get("key")
            if not key:
                return Response({"error": "كل عنصر قائمة يجب أن يحتوي على key"}, status=400)
            try:
                item = DashboardNavigationItem.objects.get(key=key)
            except DashboardNavigationItem.DoesNotExist:
                return Response({"error": f"عنصر القائمة غير معروف: {key}"}, status=400)
            for field in nav_fields:
                if field in payload:
                    setattr(item, field, payload[field])
            item.save()

        for payload in metrics:
            key = payload.get("key")
            if not key:
                return Response({"error": "كل بطاقة مؤشر يجب أن تحتوي على key"}, status=400)
            try:
                item = DashboardMetricCard.objects.get(key=key)
            except DashboardMetricCard.DoesNotExist:
                return Response({"error": f"بطاقة المؤشر غير معروفة: {key}"}, status=400)
            for field in metric_fields:
                if field in payload:
                    setattr(item, field, payload[field])
            item.save()

        return Response({
            "navigation": serialize_navigation(request.user, include_inactive=True),
            "metrics": serialize_metrics(include_inactive=True),
        })


class AssistantView(APIView):
    def post(self, request):
        question = str(request.data.get("message", "")).strip()
        if not question:
            return Response({"error": "اكتب سؤالك أولًا"}, status=400)
        normalized = question.lower()
        if "متأخر" in normalized or "pending" in normalized:
            answer = f"يوجد {Thesis.objects.exclude(status='COMPLETED').count()} ملفًا قيد المتابعة."
        elif "مناقش" in normalized or "defense" in normalized:
            answer = f"إجمالي لجان المناقشة المسجلة حاليًا {DefenseCommittee.objects.count()}."
        elif "طالب" in normalized or "student" in normalized:
            answer = f"إجمالي الطلاب المسجلين في النظام {Student.objects.count()}."
        else:
            answer = "أستطيع مساعدتك في الطلاب والرسائل والمناقشات والملفات المتأخرة والتقارير."
        return Response({
            "answer": answer,
            "role": request.user.role,
            "requires_confirmation": False,
            "source": "authorized_system_data",
        })
