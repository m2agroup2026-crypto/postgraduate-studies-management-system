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
