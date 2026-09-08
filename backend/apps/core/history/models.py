from django.db import models


class AcademicHistoryEvent(models.Model):
    class EventType(models.TextChoices):
        ENROLLMENT_CREATED = "ENROLLMENT_CREATED", "إنشاء قيد أكاديمي"
        ENROLLMENT_UPDATED = "ENROLLMENT_UPDATED", "تحديث القيد الأكاديمي"
        THESIS_REGISTERED = "THESIS_REGISTERED", "تسجيل الرسالة العلمية"
        THESIS_STATUS_CHANGED = "THESIS_STATUS_CHANGED", "تغيير حالة الرسالة"
        DOCUMENT_UPLOADED = "DOCUMENT_UPLOADED", "رفع مستند"
        DEFENSE_CREATED = "DEFENSE_CREATED", "إنشاء لجنة مناقشة"
        DEFENSE_COMPLETED = "DEFENSE_COMPLETED", "إتمام المناقشة"
        OTHER = "OTHER", "حدث آخر"

    student = models.ForeignKey(
        "students.Student",
        on_delete=models.PROTECT,
        related_name="history_events",
    )

    event_type = models.CharField(
        max_length=100,
        choices=EventType.choices,
    )

    title_ar = models.CharField(
        max_length=255,
    )

    description_ar = models.TextField(
        blank=True,
    )

    reference_type = models.CharField(
        max_length=100,
        blank=True,
    )

    reference_id = models.PositiveBigIntegerField(
        null=True,
        blank=True,
    )

    performed_by = models.ForeignKey(
        "accounts.User",
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name="academic_history_events",
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    class Meta:
        app_label = "core"
        ordering = ["-created_at", "-id"]

    def __str__(self):
        return self.title_ar
