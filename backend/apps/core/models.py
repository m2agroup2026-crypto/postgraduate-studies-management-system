from django.db import models


class Role(models.Model):
    name = models.CharField(
        max_length=100,
        unique=True
    )

    permissions = models.ManyToManyField("Permission", blank=True)

    name_ar = models.CharField(
        max_length=150
    )

    name_en = models.CharField(
        max_length=150,
        blank=True
    )

    is_active = models.BooleanField(
        default=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return self.name_ar


class Permission(models.Model):
    code = models.CharField(
        max_length=100,
        unique=True
    )

    name_ar = models.CharField(
        max_length=150
    )

    name_en = models.CharField(
        max_length=150,
        blank=True
    )

    description_ar = models.TextField(
        blank=True
    )

    description_en = models.TextField(
        blank=True
    )

    is_active = models.BooleanField(
        default=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return self.name_ar


class ApprovalAction(models.Model):
    class ActionType(models.TextChoices):
        SUBMIT = "SUBMIT", "تقديم"
        REVIEW = "REVIEW", "مراجعة"
        APPROVE = "APPROVE", "اعتماد"
        REJECT = "REJECT", "رفض"
        RETURN = "RETURN", "إعادة للتعديل"

    request_type = models.CharField(
        max_length=100
    )

    object_id = models.PositiveBigIntegerField()

    action = models.CharField(
        max_length=20,
        choices=ActionType.choices
    )

    from_status = models.CharField(
        max_length=50,
        blank=True
    )

    to_status = models.CharField(
        max_length=50,
        blank=True
    )

    performed_by = models.ForeignKey(
        "accounts.User",
        on_delete=models.PROTECT,
        related_name="approval_actions"
    )

    notes = models.TextField(
        blank=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.request_type} - {self.action}"


class WorkflowStatus(models.Model):
    code = models.CharField(
        max_length=50,
        unique=True
    )

    name_ar = models.CharField(
        max_length=150
    )

    name_en = models.CharField(
        max_length=150,
        blank=True
    )

    description_ar = models.TextField(
        blank=True
    )

    is_active = models.BooleanField(
        default=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        ordering = ["code"]

    def __str__(self):
        return self.name_ar
