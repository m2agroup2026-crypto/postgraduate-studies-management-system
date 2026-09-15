"""Facade preserving the original assistant API over modular domain services."""

from datetime import date

from apps.committees.models import DefenseCommittee
from apps.core.authorization import has_permission
from apps.students.models import Student
from apps.theses.models import Thesis

from .router import detect_intent, general_ai_answer
from .services import analytics, committees, language_for, response, students, theses, workflow

SERVICES = {
    "students": students.handle,
    "theses": theses.handle,
    "committees": committees.handle,
    "workflow": workflow.handle,
    "analytics": analytics.handle,
}


def executive_brief(user):
    metrics = {}
    if has_permission(user, "students.view"):
        metrics["students"] = Student.objects.count()
    if has_permission(user, "theses.view"):
        metrics["theses"] = Thesis.objects.count()
    if has_permission(user, "committees.view"):
        metrics["committees"] = DefenseCommittee.objects.count()
    return {
        "title": "Academic Intelligence Brief",
        "user": {
            "name": getattr(user, "effective_name", user.username),
            "role": user.role,
        },
        "metrics": metrics,
        "system_status": "Operational",
        "insights": [
            "Live academic data connected",
            "Permission-based intelligence enabled",
        ],
        "generated_at": str(date.today()),
    }


def process_request(command, user):
    language = language_for(command)
    intent = detect_intent(command)
    service = SERVICES.get(intent)
    if service:
        return service(command, user, language)
    return response("general", general_ai_answer(command, language), {"authorized": True})


def process_command(command, user):
    """Backward-compatible string response used by existing integrations."""
    return process_request(command, user)["answer"]
