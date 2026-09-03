from django.core.management.base import BaseCommand

from apps.core.models import WorkflowStatus


class Command(BaseCommand):
    help = "Seed workflow statuses"

    def handle(self, *args, **options):
        statuses = [
            {
                "code": "REGISTERED",
                "name_ar": "مسجل",
                "name_en": "Registered",
            },
            {
                "code": "DRAFT",
                "name_ar": "مسودة",
                "name_en": "Draft",
            },
            {
                "code": "SUBMITTED",
                "name_ar": "تم التقديم",
                "name_en": "Submitted",
            },
            {
                "code": "UNDER_REVIEW",
                "name_ar": "تحت المراجعة",
                "name_en": "Under Review",
            },
            {
                "code": "APPROVED",
                "name_ar": "معتمد",
                "name_en": "Approved",
            },
            {
                "code": "REJECTED",
                "name_ar": "مرفوض",
                "name_en": "Rejected",
            },
            {
                "code": "RETURNED",
                "name_ar": "معاد للتعديل",
                "name_en": "Returned",
            },
        ]

        for status in statuses:
            WorkflowStatus.objects.update_or_create(
                code=status["code"],
                defaults=status,
            )

        self.stdout.write(
            self.style.SUCCESS(
                "Workflow statuses seeded successfully"
            )
        )
