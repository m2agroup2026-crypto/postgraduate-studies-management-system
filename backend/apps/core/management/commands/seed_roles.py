from django.core.management.base import BaseCommand
from django.db import transaction

from apps.accounts.models import User
from apps.core.models import Permission, Role

STANDARD_PERMISSIONS = {
    "dashboard.manage": "إدارة إعدادات المنصة",
    "roles.manage": "إدارة الأدوار",
    "permissions.manage": "إدارة الصلاحيات",
    "users.manage": "إدارة المستخدمين",
    "students.view": "عرض الطلاب",
    "students.create": "إضافة الطلاب",
    "students.update": "تعديل بيانات الطلاب",
    "students.manage": "إدارة بيانات الطلاب",
    "theses.view": "عرض الرسائل العلمية",
    "theses.create": "إضافة الرسائل العلمية",
    "theses.update": "تعديل الرسائل العلمية",
    "theses.manage": "إدارة الرسائل العلمية",
    "committees.view": "عرض اللجان والمناقشات",
    "committees.create": "إنشاء اللجان",
    "committees.update": "تعديل اللجان والمناقشات",
    "committees.manage": "إدارة اللجان والمناقشات",
    "reports.view": "عرض التقارير",
    "reports.export": "تصدير التقارير",
    "registration.create": "إنشاء طلب تسجيل",
    "registration.review": "مراجعة طلب التسجيل",
    "registration.approve": "اعتماد طلب التسجيل",
    "committee.approve": "اعتماد اللجنة",
}

PLATFORM_PERMISSIONS = {
    "dashboard.manage",
    "roles.manage",
    "permissions.manage",
    "users.manage",
}

PROGRAM_PERMISSIONS = {
    "students.view",
    "students.create",
    "students.update",
    "students.manage",
    "theses.view",
    "theses.create",
    "theses.update",
    "theses.manage",
    "committees.view",
    "committees.create",
    "committees.update",
    "committees.manage",
    "reports.view",
    "reports.export",
    "registration.create",
    "registration.review",
    "registration.approve",
    "committee.approve",
}

ROLE_MATRIX = {
    "PLATFORM_ADMIN": ("مدير المنصة الرقمية", PLATFORM_PERMISSIONS),
    "PROGRAM_DIRECTOR": ("مدير البرنامج", PROGRAM_PERMISSIONS),
    "POSTGRADUATE_DIRECTOR": (
        "مدير الدراسات العليا",
        {
            "students.view",
            "students.manage",
            "theses.view",
            "theses.manage",
            "committees.view",
            "committees.manage",
            "reports.view",
            "reports.export",
            "registration.approve",
            "committee.approve",
        },
    ),
    "VICE_DEAN_POSTGRADUATE": (
        "وكيل الكلية لشئون الدراسات العليا والبحوث",
        {
            "students.view",
            "theses.view",
            "committees.view",
            "reports.view",
            "registration.approve",
            "committee.approve",
        },
    ),
    "DEAN": (
        "عميد الكلية",
        {"students.view", "theses.view", "committees.view", "reports.view"},
    ),
    "VP_POSTGRADUATE_RESEARCH": (
        "نائب رئيس الجامعة لشئون الدراسات العليا والبحوث",
        {
            "students.view",
            "theses.view",
            "committees.view",
            "reports.view",
            "reports.export",
        },
    ),
    "STAFF": (
        "موظف إدخال البيانات",
        {
            "students.view",
            "students.create",
            "students.update",
            "theses.view",
            "registration.create",
        },
    ),
    "REVIEWER": (
        "مراجع",
        {"students.view", "theses.view", "registration.review"},
    ),
    "SUPERVISOR": ("مشرف", {"students.view", "theses.view"}),
    "STUDENT": ("طالب", {"theses.view"}),
}

ACCOUNT_BINDINGS = {
    "ahmed": {"PLATFORM_ADMIN", "PROGRAM_DIRECTOR"},
    "vice_dean": {"VICE_DEAN_POSTGRADUATE"},
}


class Command(BaseCommand):
    help = "Create the canonical, idempotent role and permission matrix"

    @transaction.atomic
    def handle(self, *args, **options):
        permission_map = {}
        for code, name_ar in STANDARD_PERMISSIONS.items():
            permission, _ = Permission.objects.update_or_create(
                code=code,
                defaults={"name_ar": name_ar, "name_en": code, "is_active": True},
            )
            permission_map[code] = permission

        role_map = {}
        for role_name, (name_ar, permission_codes) in ROLE_MATRIX.items():
            role, _ = Role.objects.update_or_create(
                name=role_name,
                defaults={"name_ar": name_ar, "name_en": role_name, "is_active": True},
            )
            role.permissions.set(permission_map[code] for code in permission_codes)
            role_map[role_name] = role

        platform_role = role_map["PLATFORM_ADMIN"]
        for user in User.objects.filter(roles=platform_role).exclude(username="ahmed"):
            user.roles.remove(platform_role)

        for username, role_names in ACCOUNT_BINDINGS.items():
            user = User.objects.filter(username__iexact=username).first()
            if user:
                user.roles.set(role_map[name] for name in role_names)

        self.stdout.write(self.style.SUCCESS("Canonical role matrix seeded successfully"))
