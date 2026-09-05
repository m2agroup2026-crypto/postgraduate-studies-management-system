from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    class Role(models.TextChoices):
        PROGRAM_DIRECTOR = "PROGRAM_DIRECTOR", "مدير البرنامج"
        POSTGRADUATE_DIRECTOR = "POSTGRADUATE_DIRECTOR", "مدير الدراسات العليا"
        DEAN = "DEAN", "عميد الكلية"
        VICE_DEAN = "VICE_DEAN", "وكيل الكلية"
        VICE_DEAN_POSTGRADUATE = "VICE_DEAN_POSTGRADUATE", "وكيل الدراسات العليا والبحوث"
        VP_POSTGRADUATE_RESEARCH = "VP_POSTGRADUATE_RESEARCH", "نائب رئيس الجامعة لشئون الدراسات العليا والبحوث"
        STAFF = "STAFF", "موظف"
        REVIEWER = "REVIEWER", "مراجع"
        SUPERVISOR = "SUPERVISOR", "مشرف"
        STUDENT = "STUDENT", "طالب"

    role = models.CharField(max_length=32, choices=Role.choices, default=Role.STAFF)
    roles = models.ManyToManyField("core.Role", blank=True, related_name="users")
    preferred_language = models.CharField(max_length=2, choices=(("ar", "العربية"), ("en", "English")), default="ar")
    display_name_ar = models.CharField(max_length=180, blank=True)
    job_title_ar = models.CharField(max_length=220, blank=True)

    def has_role(self, role_name):
        return self.roles.filter(name=role_name).exists()

    def has_permission(self, permission_code):
        return self.roles.filter(permissions__code=permission_code).exists()

    @property
    def effective_name(self):
        return self.display_name_ar or self.get_full_name() or self.username
