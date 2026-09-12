from rest_framework import serializers

from .models import AcademicDocument


class AcademicDocumentSerializer(serializers.ModelSerializer):
    student_name = serializers.CharField(
        source="student.name_ar",
        read_only=True,
    )

    uploaded_by_name = serializers.CharField(
        source="uploaded_by.username",
        read_only=True,
    )

    class Meta:
        model = AcademicDocument
        fields = [
            "id",
            "student",
            "student_name",
            "document_type",
            "title",
            "file",
            "original_filename",
            "status",
            "upload_source",
            "reference_number",
            "document_date",
            "notes",
            "uploaded_by",
            "uploaded_by_name",
            "created_at",
        ]
        read_only_fields = [
            "uploaded_by",
            "created_at",
        ]
