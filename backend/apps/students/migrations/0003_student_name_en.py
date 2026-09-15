from django.db import migrations, models


def populate_english_names(apps, schema_editor):
    Student = apps.get_model("students", "Student")
    from apps.students.names import transliterate_arabic_name
    for student in Student.objects.filter(name_en="").iterator():
        student.name_en = transliterate_arabic_name(student.name_ar)
        student.save(update_fields=["name_en"])

class Migration(migrations.Migration):
    dependencies = [("students", "0002_academicenrollment_academicenrollmentevent")]
    operations = [
        migrations.AddField(
            model_name="student",
            name="name_en",
            field=models.CharField(blank=True, db_index=True, max_length=200),
        ),
        migrations.RunPython(populate_english_names, migrations.RunPython.noop),
    ]
