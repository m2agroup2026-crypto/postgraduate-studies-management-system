from django.shortcuts import get_object_or_404

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

from apps.theses.models import Thesis
from apps.core.services.workflow import transition


def thesis_response(thesis):
    return {
        "id": thesis.id,
        "status": thesis.status,
    }


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
            thesis_response(thesis),
            status=status.HTTP_200_OK,
        )


class ThesisReviewView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        thesis = get_object_or_404(
            Thesis,
            pk=pk
        )

        transition(
            obj=thesis,
            action="REVIEW",
            user=request.user,
            notes="Thesis sent for review",
        )

        return Response(
            thesis_response(thesis),
            status=status.HTTP_200_OK,
        )


class ThesisDirectorApproveView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        thesis = get_object_or_404(
            Thesis,
            pk=pk
        )

        transition(
            obj=thesis,
            action="DIRECTOR_APPROVE",
            user=request.user,
            notes="Approved by postgraduate director",
        )

        return Response(
            thesis_response(thesis),
            status=status.HTTP_200_OK,
        )


class ThesisViceDeanApproveView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        thesis = get_object_or_404(
            Thesis,
            pk=pk
        )

        transition(
            obj=thesis,
            action="VICE_DEAN_APPROVE",
            user=request.user,
            notes="Approved by vice dean postgraduate",
        )

        return Response(
            thesis_response(thesis),
            status=status.HTTP_200_OK,
        )


class ThesisDeanApproveView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        thesis = get_object_or_404(
            Thesis,
            pk=pk
        )

        transition(
            obj=thesis,
            action="DEAN_APPROVE",
            user=request.user,
            notes="Approved by dean",
        )

        return Response(
            thesis_response(thesis),
            status=status.HTTP_200_OK,
        )


class ThesisFinalApproveView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        thesis = get_object_or_404(
            Thesis,
            pk=pk
        )

        transition(
            obj=thesis,
            action="FINAL_APPROVE",
            user=request.user,
            notes="Final approval by VP postgraduate research",
        )

        return Response(
            thesis_response(thesis),
            status=status.HTTP_200_OK,
        )
