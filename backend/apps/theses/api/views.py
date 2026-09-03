from django.shortcuts import get_object_or_404

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

from apps.theses.models import Thesis
from apps.core.services.workflow import transition


class ThesisSubmitView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        thesis = get_object_or_404(
            Thesis,
            pk=pk
        )

        transition(
            obj=thesis,
            action="SUBMIT",
            user=request.user,
            notes="Thesis submitted through API",
        )

        return Response(
            {
                "id": thesis.id,
                "status": thesis.status,
            },
            status=status.HTTP_200_OK,
        )
