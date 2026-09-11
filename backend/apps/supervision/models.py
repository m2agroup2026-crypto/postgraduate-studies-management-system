from django.db import models


class SupervisorProfile(models.Model):
    user = models.OneToOneField(
        "accounts.User",
        on_delete=models.PROTECT,
        related_name="supervisor_profile",
        null=True,
        blank=True,
    )

    department = models.ForeignKey(
        "academics.Department",
        on_delete=models.PROTECT,
        related_name="supervisors",
        null=True,
        blank=True,
    )

    name_ar = models.CharField(max_length=200)
    name_en = models.CharField(max_length=200, blank=True)

    academic_rank = models.CharField(
        max_length=100,
        blank=True,
    )

    specialization = models.CharField(
        max_length=200,
        blank=True,
    )

    is_external = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name_ar

class ThesisSupervisorAssignment(models.Model):
    class SupervisorRole(models.TextChoices):
        PRIMARY_SUPERVISOR = "PRIMARY_SUPERVISOR", "مشرف رئيسي"
        CO_SUPERVISOR = "CO_SUPERVISOR", "مشرف مشارك"
        EXTERNAL_SUPERVISOR = "EXTERNAL_SUPERVISOR", "مشرف خارجي"
        ASSISTANT_SUPERVISOR = "ASSISTANT_SUPERVISOR", "مشرف مساعد"

    class AssignmentStatus(models.TextChoices):
        PENDING_APPROVAL = "PENDING_APPROVAL", "بانتظار الاعتماد"
        ACTIVE = "ACTIVE", "نشط"
        ENDED = "ENDED", "منتهي"
        REPLACED = "REPLACED", "تم الاستبدال"

    thesis = models.ForeignKey(
        "theses.Thesis",
        on_delete=models.PROTECT,
        related_name="supervisor_assignments",
    )

    supervisor = models.ForeignKey(
        SupervisorProfile,
        on_delete=models.PROTECT,
        related_name="thesis_assignments",
    )

    role = models.CharField(
        max_length=50,
        choices=SupervisorRole.choices,
    )

    status = models.CharField(
        max_length=50,
        choices=AssignmentStatus.choices,
        default=AssignmentStatus.PENDING_APPROVAL,
    )

    start_date = models.DateField(
        null=True,
        blank=True,
    )

    end_date = models.DateField(
        null=True,
        blank=True,
    )

    approved_by = models.ForeignKey(
        "accounts.User",
        on_delete=models.PROTECT,
        related_name="approved_supervision_assignments",
        null=True,
        blank=True,
    )

    approved_at = models.DateTimeField(
        null=True,
        blank=True,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    updated_at = models.DateTimeField(
        auto_now=True,
    )

    def __str__(self):
        return f"{self.thesis_id} - {self.supervisor}"

class SupervisorChangeRequest(models.Model):
    class RequestStatus(models.TextChoices):
        DRAFT = "DRAFT", "مسودة"
        SUBMITTED = "SUBMITTED", "تم التقديم"
        UNDER_REVIEW = "UNDER_REVIEW", "تحت المراجعة"
        APPROVED = "APPROVED", "معتمد"
        REJECTED = "REJECTED", "مرفوض"
        COMPLETED = "COMPLETED", "مكتمل"

    thesis = models.ForeignKey(
        "theses.Thesis",
        on_delete=models.PROTECT,
        related_name="supervisor_change_requests",
    )

    current_assignment = models.ForeignKey(
        ThesisSupervisorAssignment,
        on_delete=models.PROTECT,
        related_name="change_requests",
    )

    requested_supervisor = models.ForeignKey(
        SupervisorProfile,
        on_delete=models.PROTECT,
        related_name="requested_supervisor_changes",
    )

    reason = models.TextField()

    status = models.CharField(
        max_length=50,
        choices=RequestStatus.choices,
        default=RequestStatus.DRAFT,
    )

    requested_by = models.ForeignKey(
        "accounts.User",
        on_delete=models.PROTECT,
        related_name="supervisor_change_requests_created",
    )

    reviewed_by = models.ForeignKey(
        "accounts.User",
        on_delete=models.PROTECT,
        related_name="supervisor_change_requests_reviewed",
        null=True,
        blank=True,
    )

    decision_notes = models.TextField(
        blank=True,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    updated_at = models.DateTimeField(
        auto_now=True,
    )

    def __str__(self):
        return f"Supervisor change request - {self.thesis_id}"

