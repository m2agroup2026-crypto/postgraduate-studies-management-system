from math import ceil

from django.db.models import Q
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.theses.models import Thesis

from .models import Student

VIEW_PERMISSION = "students.view"
MANAGE_PERMISSION = "students.manage"

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


def has_capability(user, permission_code, legacy_roles):
    """Prefer database roles and fall back to the legacy enum during migration."""
    if user.is_superuser or user.is_staff:
        return True

    active_roles = user.roles.filter(is_active=True)
    if active_roles.exists():
        return active_roles.filter(
            permissions__code=permission_code,
            permissions__is_active=True,
        ).exists()

    return user.role in legacy_roles


def can_view_students(user):
    return has_capability(user, VIEW_PERMISSION, LEGACY_VIEW_ROLES)


def can_manage_students(user):
    return has_capability(user, MANAGE_PERMISSION, LEGACY_MANAGE_ROLES)


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


def mask_national_id(value):
    if not value:
        return ""
    if len(value) <= 4:
        return "*" * len(value)
    return f"{value[:2]}{'*' * (len(value) - 4)}{value[-2:]}"


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


def get_thesis(student):
    try:
        return student.thesis
    except Thesis.DoesNotExist:
        return None


def serialize_student(student, include_sensitive=False):
    thesis = get_thesis(student)
    payload = {
        "id": student.id,
        "university_id": student.university_id,
        "name_ar": student.name_ar,
        "national_id_masked": mask_national_id(student.national_id),
        "department": serialize_department(student.department),
        "thesis": (
            {
                "id": thesis.id,
                "title_ar": thesis.title_ar,
                "status": thesis.status,
            }
            if thesis
            else None
        ),
    }
    if include_sensitive:
        payload["national_id"] = student.national_id
    return payload


def student_queryset():
    return Student.objects.select_related(
        "department",
        "department__faculty",
        "department__faculty__university",
        "thesis",
    )


class StudentCollectionView(APIView):
    def get(self, request):
        if not can_view_students(request.user):
            return Response({"error": "غير مصرح لك بعرض بيانات الطلاب"}, status=403)

        queryset = student_queryset()
        search = request.query_params.get("q", "").strip()
        department_id = request.query_params.get("department", "").strip()
        thesis_status = request.query_params.get("thesis_status", "").strip()

        if search:
            queryset = queryset.filter(
                Q(university_id__icontains=search)
                | Q(name_ar__icontains=search)
                | Q(national_id__icontains=search)
                | Q(department__name_ar__icontains=search)
                | Q(department__name_en__icontains=search)
            )
        if department_id:
            queryset = queryset.filter(department_id=department_id)
        if thesis_status:
            if thesis_status == "NO_THESIS":
                queryset = queryset.filter(thesis__isnull=True)
            else:
                queryset = queryset.filter(thesis__status=thesis_status)

        ordering = request.query_params.get("ordering", "university_id")
        ordering_map = {
            "university_id": "university_id",
            "-university_id": "-university_id",
            "name": "name_ar",
            "-name": "-name_ar",
            "department": "department__name_ar",
            "-department": "-department__name_ar",
        }
        queryset = queryset.order_by(ordering_map.get(ordering, "university_id"), "id")

        page = parse_positive_int(request.query_params.get("page"), 1)
        page_size = parse_positive_int(request.query_params.get("page_size"), 20, 100)
        total = queryset.count()
        pages = max(1, ceil(total / page_size)) if total else 0
        if pages and page > pages:
            page = pages
        start = (page - 1) * page_size
        end = start + page_size

        department_options = list(
            Student.objects.values(
                "department_id",
                "department__code",
                "department__name_ar",
                "department__name_en",
            )
            .distinct()
            .order_by("department__name_ar")
        )
        thesis_statuses = list(
            Student.objects.exclude(thesis__isnull=True)
            .values_list("thesis__status", flat=True)
            .distinct()
            .order_by("thesis__status")
        )

        return Response(
            {
                "results": [serialize_student(student) for student in queryset[start:end]],
                "pagination": {
                    "page": page,
                    "page_size": page_size,
                    "total": total,
                    "pages": pages,
                },
                "filters": {
                    "departments": department_options,
                    "thesis_statuses": thesis_statuses,
                },
                "capabilities": {
                    "can_view": True,
                    "can_manage": can_manage_students(request.user),
                },
            }
        )


class StudentDetailView(APIView):
    def get(self, request, student_id):
        if not can_view_students(request.user):
            return Response({"error": "غير مصرح لك بعرض بيانات الطلاب"}, status=403)

        try:
            student = student_queryset().get(pk=student_id)
        except Student.DoesNotExist:
            return Response({"error": "سجل الطالب غير موجود"}, status=404)

        can_manage = can_manage_students(request.user)
        return Response(
            {
                "student": serialize_student(student, include_sensitive=can_manage),
                "capabilities": {
                    "can_view": True,
                    "can_manage": can_manage,
                },
            }
        )
