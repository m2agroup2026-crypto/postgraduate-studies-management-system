from django.db import models


class Role(models.Model):
    name = models.CharField(max_length=100, unique=True)
    permissions = models.ManyToManyField("Permission", blank=True)
    name_ar = models.CharField(max_length=150)
    name_en = models.CharField(max_length=150, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name_ar


class Permission(models.Model):
    code = models.CharField(max_length=100, unique=True)
    name_ar = models.CharField(max_length=150)
    name_en = models.CharField(max_length=150, blank=True)
    description_ar = models.TextField(blank=True)
    description_en = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name_ar


class DashboardNavigationItem(models.Model):
    key = models.SlugField(max_length=80, unique=True)
    label_ar = models.CharField(max_length=150)
    label_en = models.CharField(max_length=150, blank=True)
    route = models.CharField(max_length=180, default="/")
    icon = models.CharField(max_length=60, blank=True, default="LayoutDashboard")
    required_permission = models.CharField(max_length=100, blank=True)
    sort_order = models.PositiveSmallIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["sort_order", "id"]

    def __str__(self):
        return self.label_ar


class DashboardMetricCard(models.Model):
    class MetricKey(models.TextChoices):
        STUDENTS = "students", "الطلاب النشطون"
        THESES = "theses", "الرسائل المسجلة"
        DEFENSES = "defenses", "المناقشات القادمة"
        PENDING = "pending", "ملفات تحتاج متابعة"

    key = models.CharField(max_length=32, choices=MetricKey.choices, unique=True)
    label_ar = models.CharField(max_length=150)
    label_en = models.CharField(max_length=150, blank=True)
    icon = models.CharField(max_length=60, blank=True)
    sort_order = models.PositiveSmallIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["sort_order", "id"]

    def __str__(self):
        return self.label_ar


class ApprovalAction(models.Model):
    class ActionType(models.TextChoices):
        SUBMIT = "SUBMIT", "تقديم"
        REVIEW = "REVIEW", "مراجعة"
        APPROVE = "APPROVE", "اعتماد"
        DIRECTOR_APPROVE = "DIRECTOR_APPROVE", "اعتماد مدير الدراسات العليا"
        VICE_DEAN_APPROVE = "VICE_DEAN_APPROVE", "اعتماد وكيل الدراسات العليا"
        DEAN_APPROVE = "DEAN_APPROVE", "اعتماد العميد"
        FINAL_APPROVE = "FINAL_APPROVE", "الاعتماد النهائي"
        REJECT = "REJECT", "رفض"
        RETURN = "RETURN", "إعادة للتعديل"

    request_type = models.CharField(max_length=100)
    object_id = models.PositiveBigIntegerField()
    action = models.CharField(max_length=20, choices=ActionType.choices)
    from_status = models.CharField(max_length=50, blank=True)
    to_status = models.CharField(max_length=50, blank=True)
    performed_by = models.ForeignKey(
        "accounts.User",
        on_delete=models.PROTECT,
        related_name="approval_actions",
    )
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.request_type} - {self.action}"


class WorkflowStatus(models.Model):
    code = models.CharField(max_length=50, unique=True)
    name_ar = models.CharField(max_length=150)
    name_en = models.CharField(max_length=150, blank=True)
    description_ar = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["code"]

    def __str__(self):
        return self.name_ar

