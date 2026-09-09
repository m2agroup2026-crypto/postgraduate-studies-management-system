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
