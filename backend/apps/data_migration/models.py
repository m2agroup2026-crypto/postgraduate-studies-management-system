from django.db import models


class LegacyImportBatch(models.Model):
    class Status(models.TextChoices):
        CREATED = "CREATED", "Created"
        VALIDATING = "VALIDATING", "Validating"
        READY = "READY", "Ready"
        IMPORTED = "IMPORTED", "Imported"
        FAILED = "FAILED", "Failed"

    source_file = models.CharField(max_length=255)

    source_type = models.CharField(max_length=50, default="EXCEL")

    source_checksum = models.CharField(max_length=64, blank=True, db_index=True)

    status = models.CharField(max_length=20, choices=Status.choices, default=Status.CREATED)

    total_records = models.PositiveIntegerField(default=0)

    processed_records = models.PositiveIntegerField(default=0)

    failed_records = models.PositiveIntegerField(default=0)

    analysis_result = models.JSONField(default=dict, blank=True)

    notes = models.TextField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.source_file} - {self.status}"


class LegacyImportRow(models.Model):
    class Status(models.TextChoices):
        VALID = "VALID", "Valid"
        IMPORTED = "IMPORTED", "Imported"
        UPDATED = "UPDATED", "Updated"
        SKIPPED = "SKIPPED", "Skipped"
        FAILED = "FAILED", "Failed"

    batch = models.ForeignKey(
        LegacyImportBatch,
        on_delete=models.CASCADE,
        related_name="rows",
    )
    sheet_name = models.CharField(max_length=255)
    source_row_number = models.PositiveIntegerField()
    source_identifier = models.CharField(max_length=100)
    row_checksum = models.CharField(max_length=64)
    raw_payload = models.JSONField(default=dict)
    status = models.CharField(max_length=20, choices=Status.choices)
    errors = models.JSONField(default=list, blank=True)
    student = models.ForeignKey(
        "students.Student",
        on_delete=models.PROTECT,
        related_name="legacy_import_rows",
        null=True,
        blank=True,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["source_row_number"]
        constraints = [
            models.UniqueConstraint(
                fields=["batch", "source_identifier"],
                name="unique_legacy_row_per_batch",
            )
        ]

    def __str__(self):
        return f"{self.batch_id}:{self.source_identifier}"


class LegacyFieldMapping(models.Model):
    class MappingStatus(models.TextChoices):
        PENDING = "PENDING", "Pending"
        MAPPED = "MAPPED", "Mapped"
        IGNORED = "IGNORED", "Ignored"
        REVIEW = "REVIEW", "Needs Review"

    batch = models.ForeignKey(
        LegacyImportBatch, on_delete=models.CASCADE, related_name="field_mappings"
    )

    sheet_name = models.CharField(max_length=255)

    legacy_field = models.CharField(max_length=255)

    target_model = models.CharField(max_length=255, blank=True)

    target_field = models.CharField(max_length=255, blank=True)

    status = models.CharField(
        max_length=20, choices=MappingStatus.choices, default=MappingStatus.PENDING
    )

    notes = models.TextField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["sheet_name", "legacy_field"]

    def __str__(self):
        return self.legacy_field
