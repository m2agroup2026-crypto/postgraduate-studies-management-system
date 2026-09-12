from django.conf import settings
from django.db import models


class DocumentType(models.Model):
    code = models.CharField(max_length=100, unique=True)
    name_ar = models.CharField(max_length=150)
    name_en = models.CharField(max_length=150, blank=True)
    description_ar = models.TextField(blank=True)
    description_en = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["code"]

    def __str__(self):
        return self.name_ar


class AcademicDocument(models.Model):

    class Status(models.TextChoices):
        UPLOADED = "UPLOADED", "تم الرفع"
        UNDER_REVIEW = "UNDER_REVIEW", "قيد المراجعة"
        APPROVED = "APPROVED", "معتمد"
        REJECTED = "REJECTED", "مرفوض"

    class UploadSource(models.TextChoices):
        STAFF = "STAFF", "موظف"
        STUDENT = "STUDENT", "طالب"
        MOBILE = "MOBILE", "تطبيق الهاتف"

    student = models.ForeignKey(
        "students.Student",
        on_delete=models.PROTECT,
        related_name="documents",
        null=True,
        blank=True,
    )
    document_type = models.ForeignKey(
        DocumentType,
        on_delete=models.PROTECT,
        related_name="documents",
    )

    title = models.CharField(max_length=255)

    file = models.FileField(
        upload_to="academic_documents/"
    )

    original_filename = models.CharField(
        max_length=255,
        blank=True,
    )

    is_confidential = models.BooleanField(
        default=False,
    )

    status = models.CharField(
        max_length=30,
        choices=Status.choices,
        default=Status.UPLOADED,
    )

    upload_source = models.CharField(
        max_length=30,
        choices=UploadSource.choices,
        default=UploadSource.STAFF,
    )

    reference_number = models.CharField(
        max_length=100,
        blank=True,
    )

    document_date = models.DateField(
        null=True,
        blank=True,
    )

    notes = models.TextField(blank=True)

    uploaded_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="uploaded_academic_documents",
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.title
