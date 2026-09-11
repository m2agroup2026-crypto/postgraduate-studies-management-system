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
