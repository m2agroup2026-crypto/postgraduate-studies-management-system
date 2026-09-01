from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    class Role(models.TextChoices):
        PROGRAM_DIRECTOR = "PROGRAM_DIRECTOR", "مدير البرنامج"
        DEAN = "DEAN", "عميد الكلية"
        VICE_DEAN = "VICE_DEAN", "وكيل الكلية"
        STAFF = "STAFF", "موظف"
        SUPERVISOR = "SUPERVISOR", "مشرف"
        STUDENT = "STUDENT", "طالب"

    role = models.CharField(max_length=32, choices=Role.choices, default=Role.STAFF)
    preferred_language = models.CharField(max_length=2, choices=(("ar", "العربية"), ("en", "English")), default="ar")
    display_name_ar = models.CharField(max_length=180, blank=True)
    job_title_ar = models.CharField(max_length=220, blank=True)

    @property
    def effective_name(self):
        return self.display_name_ar or self.get_full_name() or self.username
