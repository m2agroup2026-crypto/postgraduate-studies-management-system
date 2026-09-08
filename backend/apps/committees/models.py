from django.db import models

from apps.theses.models import Thesis


class DefenseCommittee(models.Model):
    thesis = models.OneToOneField(Thesis, on_delete=models.PROTECT)
    defense_date = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=50, default="SCHEDULED")


class DefenseScheduleEvent(models.Model):
    class EventType(models.TextChoices):
        SCHEDULED = "SCHEDULED", "تمت الجدولة"
        RESCHEDULED = "RESCHEDULED", "إعادة جدولة"
        DATE_CLEARED = "DATE_CLEARED", "إلغاء تاريخ المناقشة"

    committee = models.ForeignKey(
        DefenseCommittee,
        on_delete=models.CASCADE,
        related_name="schedule_events",
    )
    event_type = models.CharField(max_length=20, choices=EventType.choices)
    old_date = models.DateField(null=True, blank=True)
    new_date = models.DateField(null=True, blank=True)
    performed_by = models.ForeignKey(
        "accounts.User",
        on_delete=models.PROTECT,
        related_name="defense_schedule_events",
    )
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at", "-id"]

    def __str__(self):
        return f"{self.committee_id} - {self.event_type}"
