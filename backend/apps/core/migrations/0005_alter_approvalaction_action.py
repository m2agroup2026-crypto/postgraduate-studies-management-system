from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [("core", "0004_dashboard_configuration")]

    operations = [
        migrations.AlterField(
            model_name="approvalaction",
            name="action",
            field=models.CharField(
                choices=[
                    ("SUBMIT", "تقديم"),
                    ("REVIEW", "مراجعة"),
                    ("APPROVE", "اعتماد"),
                    ("DIRECTOR_APPROVE", "اعتماد مدير الدراسات العليا"),
                    ("VICE_DEAN_APPROVE", "اعتماد وكيل الدراسات العليا"),
                    ("DEAN_APPROVE", "اعتماد العميد"),
                    ("FINAL_APPROVE", "الاعتماد النهائي"),
                    ("REJECT", "رفض"),
                    ("RETURN", "إعادة للتعديل"),
                ],
                max_length=20,
            ),
        ),
    ]
