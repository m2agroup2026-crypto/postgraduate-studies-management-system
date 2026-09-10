import os

from django.core.management import call_command
from django.core.management.base import BaseCommand
from django.db import transaction

from apps.academics.models import AcademicDegree, Department
from apps.accounts.models import User
from apps.students.models import Student
from apps.theses.models import Thesis


def enabled(name):
    return os.environ.get(name, "").strip().lower() in {"1", "true", "yes", "on"}


class Command(BaseCommand):
    help = "Create optional development demonstration accounts and records"

    def add_arguments(self, parser):
        parser.add_argument(
            "--reset-passwords",
            action="store_true",
            help="Explicitly reset passwords for existing demonstration accounts",
        )

    @transaction.atomic
    def handle(self, *args, **options):
        if not enabled("PGMS_SEED_DEMO"):
            self.stdout.write("Demo seed skipped; set PGMS_SEED_DEMO=true to enable it")
            return

        demo_password = os.environ.get("PGMS_DEMO_PASSWORD")
        if not demo_password:
            raise RuntimeError("PGMS_DEMO_PASSWORD must be set when demo seed is enabled")

        users = [
            (
                "ahmed",
                User.Role.PROGRAM_DIRECTOR,
                "أحمد عبد الخالق",
                "مدير المنصة الرقمية ومدير البرنامج",
            ),
            (
                "staff_demo",
                User.Role.STAFF,
                "موظف الدراسات العليا",
                "موظف إدخال بيانات الدراسات العليا",
            ),
            (
                "reviewer_demo",
                User.Role.REVIEWER,
                "مراجع الدراسات العليا",
                "مراجع طلبات الدراسات العليا",
            ),
            (
                "vp_postgraduate",
                User.Role.VP_POSTGRADUATE_RESEARCH,
                "الأستاذ الدكتور جمال بدر",
                "نائب رئيس الجامعة لشئون الدراسات العليا والبحوث",
            ),
            ("dean", User.Role.DEAN, "الأستاذ الدكتور علاء عطية", "عميد كلية الطب"),
            (
                "vice_dean",
                User.Role.VICE_DEAN_POSTGRADUATE,
                "الأستاذ الدكتور محمد عبد الباسط خلاف",
                "وكيل الكلية لشئون الدراسات العليا والبحوث",
            ),
        ]

        reset_passwords = options["reset_passwords"] or enabled("PGMS_RESET_DEMO_PASSWORDS")
        for username, role, name, title in users:
            user, created = User.objects.get_or_create(username=username)
            user.role = role
            user.display_name_ar = name
            user.job_title_ar = title
            update_fields = ["role", "display_name_ar", "job_title_ar"]
            if created or reset_passwords:
                user.set_password(demo_password)
                update_fields.append("password")
            user.save(update_fields=update_fields)

        call_command("seed_roles")

        department, _ = Department.objects.get_or_create(
            code="MED",
            defaults={"name_ar": "الباطنة", "name_en": "Internal Medicine"},
        )
        AcademicDegree.objects.get_or_create(code="MSC", defaults={"name_ar": "الماجستير"})
        for index in range(1, 9):
            student, _ = Student.objects.get_or_create(
                university_id=f"PG{index:04}",
                defaults={
                    "name_ar": f"طالب دراسات عليا {index}",
                    "department": department,
                },
            )
            Thesis.objects.get_or_create(
                student=student,
                defaults={
                    "title_ar": f"رسالة علمية تجريبية رقم {index}",
                    "status": "REGISTERED",
                },
            )

        self.stdout.write(self.style.SUCCESS("Optional demo data created"))
