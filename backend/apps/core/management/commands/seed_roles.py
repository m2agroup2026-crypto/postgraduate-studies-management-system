from django.core.management.base import BaseCommand
from apps.core.models import Role, Permission


class Command(BaseCommand):
    help = "Seed default roles and permissions"

    def handle(self, *args, **options):

        permissions = [
            ("users.manage", "إدارة المستخدمين"),

            ("students.view", "عرض الطلاب"),
            ("students.create", "إضافة الطلاب"),
            ("students.update", "تعديل بيانات الطلاب"),
            ("students.approve", "اعتماد الطلاب"),

            ("registration.create", "إنشاء طلب تسجيل"),
            ("registration.review", "مراجعة التسجيل"),
            ("registration.approve", "اعتماد التسجيل"),

            ("thesis.view", "عرض الرسائل"),
            ("thesis.register", "تسجيل الرسالة"),
            ("thesis.freeze", "تجميد القيد"),
            ("thesis.unfreeze", "فك تجميد القيد"),

            ("committee.create", "إنشاء لجنة"),
            ("committee.approve", "اعتماد اللجنة"),

            ("reports.view", "عرض التقارير"),
            ("reports.export", "تصدير التقارير"),
        ]

        permission_map = {}

        for code, name_ar in permissions:
            permission, _ = Permission.objects.get_or_create(
                code=code,
                defaults={
                    "name_ar": name_ar,
                    "name_en": code,
                },
            )
            permission_map[code] = permission

        roles = {
            "PROGRAM_DIRECTOR": {
                "name_ar": "مدير البرنامج",
                "permissions": list(permission_map.keys()),
            },

            "DEAN": {
                "name_ar": "عميد الكلية",
                "permissions": [
                    "reports.view",
                    "reports.export",
                    "registration.approve",
                    "committee.approve",
                ],
            },

            "VICE_DEAN_POSTGRADUATE": {
                "name_ar": "وكيل الدراسات العليا والبحوث",
                "permissions": [
                    "registration.approve",
                    "committee.approve",
                    "reports.view",
                ],
            },

            "STAFF": {
                "name_ar": "موظف إدخال البيانات",
                "permissions": [
                    "students.view",
                    "students.create",
                    "students.update",
                    "registration.create",
                ],
            },

            "REVIEWER": {
                "name_ar": "مراجع",
                "permissions": [
                    "registration.review",
                    "students.view",
                ],
            },

            "SUPERVISOR": {
                "name_ar": "مشرف",
                "permissions": [
                    "thesis.view",
                ],
            },

            "STUDENT": {
                "name_ar": "طالب",
                "permissions": [
                    "thesis.view",
                ],
            },
        }

        for role_name, data in roles.items():

            role, _ = Role.objects.get_or_create(
                name=role_name,
                defaults={
                    "name_ar": data["name_ar"],
                    "name_en": role_name,
                },
            )

            role.permissions.set(
                [
                    permission_map[p]
                    for p in data["permissions"]
                ]
            )

        self.stdout.write(
            self.style.SUCCESS(
                "Roles and permissions seeded successfully"
            )
        )
