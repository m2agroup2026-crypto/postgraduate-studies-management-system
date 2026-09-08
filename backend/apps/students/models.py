from django.db import models

from apps.academics.models import AcademicYear, Department, Program


class Student(models.Model):
    university_id = models.CharField(max_length=50, unique=True)
    name_ar = models.CharField(max_length=200)
    national_id = models.CharField(max_length=14, blank=True)
    department = models.ForeignKey(Department, on_delete=models.PROTECT)

    def __str__(self):
        return self.name_ar


class AcademicEnrollment(models.Model):
    student = models.ForeignKey(
        Student,
        on_delete=models.PROTECT,
        related_name="academic_enrollments",
    )
    program = models.ForeignKey(
        Program,
        on_delete=models.PROTECT,
        related_name="student_enrollments",
    )
    academic_year = models.ForeignKey(
        AcademicYear,
        on_delete=models.PROTECT,
        related_name="student_enrollments",
        null=True,
        blank=True,
    )
    status = models.CharField(max_length=50, default="PENDING")
    enrollment_date = models.DateField(null=True, blank=True)
    completion_date = models.DateField(null=True, blank=True)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-enrollment_date", "-id"]

    def __str__(self):
        return f"{self.student} - {self.program}"


class AcademicEnrollmentEvent(models.Model):
    enrollment = models.ForeignKey(
        AcademicEnrollment,
        on_delete=models.PROTECT,
        related_name="history",
    )
    event_type = models.CharField(max_length=50)
    from_status = models.CharField(max_length=50, blank=True)
    to_status = models.CharField(max_length=50, blank=True)
    notes = models.TextField(blank=True)
    performed_by = models.ForeignKey(
        "accounts.User",
        on_delete=models.PROTECT,
        related_name="academic_enrollment_events",
        null=True,
        blank=True,
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at", "-id"]

    def __str__(self):
        return f"{self.enrollment_id} - {self.event_type}"
