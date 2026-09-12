from django.conf import settings
from django.db import models


class PlatformSetting(models.Model):
    class ValueType(models.TextChoices):
        TEXT = "TEXT", "نص"
        NUMBER = "NUMBER", "رقم"
        BOOLEAN = "BOOLEAN", "نعم / لا"

    key = models.CharField(max_length=100, unique=True)
    value = models.TextField(blank=True)
    value_type = models.CharField(
        max_length=20,
        choices=ValueType.choices,
        default=ValueType.TEXT,
    )
    description_ar = models.CharField(max_length=255, blank=True)
    description_en = models.CharField(max_length=255, blank=True)
    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["key"]

    def __str__(self):
        return self.key


class FeatureFlag(models.Model):
    code = models.CharField(max_length=100, unique=True)
    name_ar = models.CharField(max_length=150)
    name_en = models.CharField(max_length=150, blank=True)
    description_ar = models.TextField(blank=True)
    description_en = models.TextField(blank=True)

    is_enabled = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["code"]

    def __str__(self):
        return self.code


class ConfigurationAudit(models.Model):
    action = models.CharField(max_length=100)

    entity_type = models.CharField(max_length=100)
    entity_key = models.CharField(max_length=150)

    old_value = models.TextField(blank=True)
    new_value = models.TextField(blank=True)

    performed_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="platform_configuration_changes",
    )

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.entity_type}:{self.entity_key}"


class PlatformBranding(models.Model):
    platform_name_ar = models.CharField(max_length=200)
    platform_name_en = models.CharField(max_length=200, blank=True)

    logo = models.ImageField(
        upload_to="platform/branding/",
        blank=True,
        null=True,
    )

    favicon = models.ImageField(
        upload_to="platform/branding/",
        blank=True,
        null=True,
    )

    primary_color = models.CharField(
        max_length=20,
        default="#1E3A8A",
    )

    secondary_color = models.CharField(
        max_length=20,
        default="#0F172A",
    )

    footer_credit_name = models.CharField(
        max_length=200,
        blank=True,
    )

    footer_credit_title = models.CharField(
        max_length=250,
        blank=True,
    )

    show_footer_credit = models.BooleanField(default=True)

    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "هوية المنصة"
        verbose_name_plural = "هوية المنصة"

    def __str__(self):
        return self.platform_name_ar
