import os

from django.core.management.base import BaseCommand

from apps.accounts.models import User
from apps.academics.models import AcademicDegree, Department
from apps.students.models import Student
from apps.theses.models import Thesis


class Command(BaseCommand):
    help = "Create deterministic demo users and postgraduate records"

    def handle(self, *args, **options):
        demo_password = os.environ.get("PGMS_DEMO_PASSWORD")
        if not demo_password:
            raise RuntimeError("PGMS_DEMO_PASSWORD must be set before creating demo users")
        users = [
            ("director", User.Role.PROGRAM_DIRECTOR, "مدير البرنامج", "مدير برنامج الدراسات العليا"),
            ("dean", User.Role.DEAN, "الأستاذ الدكتور علاء عطية", "عميد كلية الطب"),
            ("vice_dean", User.Role.VICE_DEAN, "الأستاذ الدكتور محمد عبد الباسط خلاف", "وكيل الكلية لشؤون الدراسات العليا والبحوث"),
        ]
        for username, role, name, title in users:
            user, _ = User.objects.get_or_create(username=username)
            user.role, user.display_name_ar, user.job_title_ar = role, name, title
            user.set_password(demo_password)
            user.save()

        department, _ = Department.objects.get_or_create(code="MED", defaults={"name_ar": "الباطنة", "name_en": "Internal Medicine"})
        AcademicDegree.objects.get_or_create(code="MSC", defaults={"name_ar": "الماجستير"})
        for index in range(1, 9):
            student, _ = Student.objects.get_or_create(university_id=f"PG{index:04}", defaults={"name_ar": f"طالب دراسات عليا {index}", "department": department})
            Thesis.objects.get_or_create(student=student, defaults={"title_ar": f"رسالة علمية تجريبية رقم {index}", "status": "REGISTERED"})
        self.stdout.write(self.style.SUCCESS("Demo data created"))
