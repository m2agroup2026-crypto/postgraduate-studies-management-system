import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("data_migration", "0002_legacyimportbatch_analysis_result_legacyfieldmapping"),
        ("students", "0002_academicenrollment_academicenrollmentevent"),
    ]

    operations = [
        migrations.AddField(
            model_name="legacyimportbatch",
            name="source_checksum",
            field=models.CharField(blank=True, db_index=True, max_length=64),
        ),
        migrations.CreateModel(
            name="LegacyImportRow",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("sheet_name", models.CharField(max_length=255)),
                ("source_row_number", models.PositiveIntegerField()),
                ("source_identifier", models.CharField(max_length=100)),
                ("row_checksum", models.CharField(max_length=64)),
                ("raw_payload", models.JSONField(default=dict)),
                ("status", models.CharField(choices=[("VALID", "Valid"), ("IMPORTED", "Imported"), ("UPDATED", "Updated"), ("SKIPPED", "Skipped"), ("FAILED", "Failed")], max_length=20)),
                ("errors", models.JSONField(blank=True, default=list)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("batch", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="rows", to="data_migration.legacyimportbatch")),
                ("student", models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name="legacy_import_rows", to="students.student")),
            ],
            options={"ordering": ["source_row_number"]},
        ),
        migrations.AddConstraint(
            model_name="legacyimportrow",
            constraint=models.UniqueConstraint(fields=("batch", "source_identifier"), name="unique_legacy_row_per_batch"),
        ),
    ]
