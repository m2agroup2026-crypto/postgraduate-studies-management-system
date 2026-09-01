from django.db.models import Count
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.committees.models import DefenseCommittee
from apps.students.models import Student
from apps.theses.models import Thesis

ROLE_IDENTITIES = {
    "DEAN": {"name": "الأستاذ الدكتور علاء عطية", "title": "عميد كلية الطب"},
    "VICE_DEAN": {"name": "الأستاذ الدكتور محمد عبد الباسط خلاف", "title": "وكيل الكلية لشؤون الدراسات العليا والبحوث"},
    "PROGRAM_DIRECTOR": {"name": "مدير البرنامج", "title": "مدير برنامج الدراسات العليا"},
}


class MeView(APIView):
    def get(self, request):
        identity = ROLE_IDENTITIES.get(request.user.role, {})
        return Response({
            "username": request.user.username,
            "role": request.user.role,
            "name": request.user.effective_name if request.user.display_name_ar else identity.get("name"),
            "title": request.user.job_title_ar or identity.get("title"),
            "language": request.user.preferred_language or "ar",
        })


class DashboardView(APIView):
    def get(self, request):
        identity = ROLE_IDENTITIES.get(request.user.role, ROLE_IDENTITIES["PROGRAM_DIRECTOR"])
        departments = list(Student.objects.values("department__name_ar").annotate(total=Count("id")).order_by("-total")[:6])
        return Response({
            "identity": identity,
            "role": request.user.role,
            "metrics": {
                "students": Student.objects.count(),
                "theses": Thesis.objects.count(),
                "defenses": DefenseCommittee.objects.count(),
                "pending": Thesis.objects.exclude(status="COMPLETED").count(),
            },
            "departments": departments,
            "alerts": [
                {"level": "warning", "text": "ملفات تحتاج مراجعة قبل اجتماع اللجنة القادم"},
                {"level": "info", "text": "مناقشات مقررة خلال الثلاثين يومًا القادمة"},
            ],
        })


class AssistantView(APIView):
    def post(self, request):
        question = str(request.data.get("message", "")).strip()
        if not question:
            return Response({"error": "اكتب سؤالك أولًا"}, status=400)
        normalized = question.lower()
        if "متأخر" in normalized or "pending" in normalized:
            answer = f"يوجد {Thesis.objects.exclude(status='COMPLETED').count()} ملفًا قيد المتابعة."
        elif "مناقش" in normalized or "defense" in normalized:
            answer = f"إجمالي لجان المناقشة المسجلة حاليًا {DefenseCommittee.objects.count()}."
        elif "طالب" in normalized or "student" in normalized:
            answer = f"إجمالي الطلاب المسجلين في النظام {Student.objects.count()}."
        else:
            answer = "أستطيع مساعدتك في الطلاب والرسائل والمناقشات والملفات المتأخرة والتقارير."
        return Response({"answer": answer, "role": request.user.role, "requires_confirmation": False, "source": "authorized_system_data"})
