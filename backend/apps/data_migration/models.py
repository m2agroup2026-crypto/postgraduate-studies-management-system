from django.db import models


class LegacyImportBatch(models.Model):
    class Status(models.TextChoices):
        CREATED = "CREATED", "Created"
        VALIDATING = "VALIDATING", "Validating"
        READY = "READY", "Ready"
        IMPORTED = "IMPORTED", "Imported"
        FAILED = "FAILED", "Failed"

    source_file = models.CharField(
        max_length=255
    )

    source_type = models.CharField(
        max_length=50,
        default="EXCEL"
    )

    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.CREATED
    )

    total_records = models.PositiveIntegerField(
        default=0
    )

    processed_records = models.PositiveIntegerField(
        default=0
    )

    failed_records = models.PositiveIntegerField(
        default=0
    )

    analysis_result = models.JSONField(
        default=dict,
        blank=True
    )

    notes = models.TextField(
        blank=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.source_file} - {self.status}"


class LegacyFieldMapping(models.Model):
    class MappingStatus(models.TextChoices):
        PENDING = "PENDING", "Pending"
        MAPPED = "MAPPED", "Mapped"
        IGNORED = "IGNORED", "Ignored"
        REVIEW = "REVIEW", "Needs Review"

    batch = models.ForeignKey(
        LegacyImportBatch,
        on_delete=models.CASCADE,
        related_name="field_mappings"
    )

    sheet_name = models.CharField(
        max_length=255
    )

    legacy_field = models.CharField(
        max_length=255
    )

    target_model = models.CharField(
        max_length=255,
        blank=True
    )

    target_field = models.CharField(
        max_length=255,
        blank=True
    )

    status = models.CharField(
        max_length=20,
        choices=MappingStatus.choices,
        default=MappingStatus.PENDING
    )

    notes = models.TextField(
        blank=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        ordering = ["sheet_name", "legacy_field"]

    def __str__(self):
        return self.legacy_field
