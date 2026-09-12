import pytest

from apps.platform_config.models import FeatureFlag, PlatformSetting


@pytest.mark.django_db
def test_feature_flag_creation():
    feature = FeatureFlag.objects.create(
        code="electronic_approval",
        name_ar="الاعتماد الإلكتروني",
        is_enabled=False,
    )

    assert feature.code == "electronic_approval"
    assert feature.is_enabled is False


@pytest.mark.django_db
def test_platform_setting_creation():
    setting = PlatformSetting.objects.create(
        key="default_language",
        value="ar",
        value_type="TEXT",
    )

    assert setting.key == "default_language"
    assert setting.value == "ar"
