from django.contrib import admin

from .models import AcademicEnrollment, AcademicEnrollmentEvent, Student


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ("university_id", "name_ar", "name_en", "department")
    search_fields = ("university_id", "name_ar", "name_en")
    list_filter = ("department",)


admin.site.register(AcademicEnrollment)
admin.site.register(AcademicEnrollmentEvent)
