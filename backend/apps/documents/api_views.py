from rest_framework.response import Response
from rest_framework.views import APIView

from apps.core.authorization import has_permission

from .models import AcademicDocument
from .serializers import AcademicDocumentSerializer


VIEW_PERMISSION = "documents.view"
MANAGE_PERMISSION = "documents.manage"


class DocumentCollectionView(APIView):

    def get(self, request):
        if not has_permission(request.user, VIEW_PERMISSION):
            return Response(
                {"error": "غير مصرح بعرض المستندات"},
                status=403,
            )

        documents = AcademicDocument.objects.select_related(
            "student",
            "document_type",
            "uploaded_by",
        )

        serializer = AcademicDocumentSerializer(
            documents,
            many=True,
        )

        return Response(
            {
                "results": serializer.data,
            }
        )

    def post(self, request):
        if not has_permission(request.user, MANAGE_PERMISSION):
            return Response(
                {"error": "غير مصرح برفع المستندات"},
                status=403,
            )

        serializer = AcademicDocumentSerializer(
            data=request.data,
        )

        serializer.is_valid(raise_exception=True)

        serializer.save(
            uploaded_by=request.user,
            upload_source=AcademicDocument.UploadSource.STAFF,
            status=AcademicDocument.Status.UPLOADED,
        )

        return Response(
            serializer.data,
            status=201,
        )
