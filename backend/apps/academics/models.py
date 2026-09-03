from django.db import models


class University(models.Model):
    code = models.CharField(max_length=20, unique=True)
    name_ar = models.CharField(max_length=200)
    name_en = models.CharField(max_length=200, blank=True)

    logo = models.ImageField(
        upload_to="universities/logos/",
        blank=True,
        null=True
    )

    address = models.TextField(blank=True)
    contact_email = models.EmailField(blank=True)
    phone = models.CharField(max_length=50, blank=True)

    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name_ar


class Faculty(models.Model):
    university = models.ForeignKey(
        University,
        on_delete=models.PROTECT,
        related_name="faculties"
    )

    code = models.CharField(max_length=20)
    name_ar = models.CharField(max_length=200)
    name_en = models.CharField(max_length=200, blank=True)

    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    class Meta:
        unique_together = ("university", "code")

    def __str__(self):
        return self.name_ar


class Department(models.Model):
    faculty = models.ForeignKey(
        Faculty,
        on_delete=models.PROTECT,
        related_name="departments",
        null=True,
        blank=True
    )

    code = models.CharField(max_length=20)
    name_ar = models.CharField(max_length=150)
    name_en = models.CharField(max_length=150, blank=True)

    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    class Meta:
        unique_together = ("faculty", "code")

    def __str__(self):
        return self.name_ar


class AcademicDegree(models.Model):
    class DegreeLevel(models.TextChoices):
        DIPLOMA = "DIPLOMA", "دبلوم"
        MASTER = "MASTER", "ماجستير"
        PHD = "PHD", "دكتوراه"

    code = models.CharField(
        max_length=20,
        unique=True
    )

    name_ar = models.CharField(
        max_length=100
    )

    name_en = models.CharField(
        max_length=100,
        blank=True
    )

    level = models.CharField(
        max_length=20,
        choices=DegreeLevel.choices,
        null=True,
        blank=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        null=True,
        blank=True
    )

    def __str__(self):
        return self.name_ar


class Program(models.Model):
    department = models.ForeignKey(
        Department,
        on_delete=models.PROTECT,
        related_name="programs"
    )

    degree = models.ForeignKey(
        AcademicDegree,
        on_delete=models.PROTECT,
        related_name="programs"
    )

    code = models.CharField(
        max_length=30
    )

    name_ar = models.CharField(
        max_length=200
    )

    name_en = models.CharField(
        max_length=200,
        blank=True
    )

    duration_years = models.PositiveIntegerField(
        default=2
    )

    is_active = models.BooleanField(
        default=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        null=True,
        blank=True
    )

    class Meta:
        unique_together = ("department", "code")

    def __str__(self):
        return self.name_ar


class AcademicYear(models.Model):
    name = models.CharField(
        max_length=20,
        unique=True
    )

    start_date = models.DateField()
    end_date = models.DateField()

    is_active = models.BooleanField(
        default=True
    )

    def __str__(self):
        return self.name


class Semester(models.Model):
    class SemesterType(models.TextChoices):
        FIRST = "FIRST", "الفصل الأول"
        SECOND = "SECOND", "الفصل الثاني"
        SUMMER = "SUMMER", "الفصل الصيفي"

    academic_year = models.ForeignKey(
        AcademicYear,
        on_delete=models.PROTECT,
        related_name="semesters"
    )

    semester_type = models.CharField(
        max_length=20,
        choices=SemesterType.choices
    )

    start_date = models.DateField()
    end_date = models.DateField()

    class Meta:
        unique_together = (
            "academic_year",
            "semester_type",
        )

    def __str__(self):
        return f"{self.academic_year} - {self.semester_type}"
