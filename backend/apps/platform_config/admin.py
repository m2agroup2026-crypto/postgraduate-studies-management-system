from django.contrib import admin

from .models import ConfigurationAudit, FeatureFlag, PlatformSetting


@admin.register(PlatformSetting)
class PlatformSettingAdmin(admin.ModelAdmin):
    list_display = (
        "key",
        "value_type",
        "is_active",
        "updated_at",
    )

    search_fields = (
        "key",
        "description_ar",
        "description_en",
    )

    list_filter = (
        "value_type",
        "is_active",
    )


@admin.register(FeatureFlag)
class FeatureFlagAdmin(admin.ModelAdmin):
    list_display = (
        "code",
        "name_ar",
        "is_enabled",
        "updated_at",
    )

    search_fields = (
        "code",
        "name_ar",
        "name_en",
    )

    list_filter = (
        "is_enabled",
    )


@admin.register(ConfigurationAudit)
class ConfigurationAuditAdmin(admin.ModelAdmin):
    list_display = (
        "entity_type",
        "entity_key",
        "action",
        "performed_by",
        "created_at",
    )

    search_fields = (
        "entity_type",
        "entity_key",
        "action",
        "performed_by__username",
    )

    readonly_fields = (
        "action",
        "entity_type",
        "entity_key",
        "old_value",
        "new_value",
        "performed_by",
        "created_at",
    )

    list_filter = (
        "entity_type",
        "action",
    )
