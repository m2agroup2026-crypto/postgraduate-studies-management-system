from datetime import date

from apps.students.models import Student
from apps.theses.models import Thesis
from apps.committees.models import DefenseCommittee

from .router import detect_intent, general_ai_answer


def executive_brief(user):

    return {
        "title": "Academic Intelligence Brief",
        "user": {
            "name": getattr(user, "name", user.username),
            "role": "Vice Dean for Postgraduate Studies and Research",
        },
        "metrics": {
            "students": Student.objects.count(),
            "theses": Thesis.objects.count(),
            "committees": DefenseCommittee.objects.count(),
        },
        "system_status": "Operational",
        "insights": [
            "Live academic data connected",
            "Permission-based intelligence enabled",
            "Executive decision support ready",
        ],
        "generated_at": str(date.today()),
    }


def process_command(command, user):

    intent = detect_intent(command)

    if intent == "general":
        return general_ai_answer(command)

    text = command.lower()

    data = executive_brief(user)
    metrics = data["metrics"]

    students = metrics["students"]
    theses = metrics["theses"]
    committees = metrics["committees"]

    # Students
    if any(word in text for word in [
        "student",
        "students",
        "طالب",
        "الطلاب",
        "عدد الطلاب",
    ]):
        return (
            f"Total postgraduate students: {students}\n\n"
            f"إجمالي طلاب الدراسات العليا المسجلين: {students}"
        )

    # Theses
    if any(word in text for word in [
        "thesis",
        "theses",
        "رسالة",
        "الرسائل",
    ]):
        return (
            f"Registered academic theses: {theses}\n\n"
            f"إجمالي الرسائل العلمية المسجلة: {theses}"
        )

    # Committees
    if any(word in text for word in [
        "committee",
        "committees",
        "defense",
        "لجنة",
        "مناقشة",
    ]):
        return (
            f"Defense committees records: {committees}\n\n"
            f"إجمالي لجان ومناقشات الدراسات العليا: {committees}"
        )

    # Meeting report
    if any(word in text for word in [
        "report",
        "meeting",
        "brief",
        "تقرير",
        "اجتماع",
        "ملخص",
    ]):
        return (
            "Executive Academic Meeting Brief\n\n"
            f"Students: {students}\n"
            f"Academic Theses: {theses}\n"
            f"Defense Committees: {committees}\n\n"
            "System Status: Operational\n"
            f"Generated: {data['generated_at']}"
        )

    # Follow up
    if any(word in text for word in [
        "pending",
        "follow",
        "متابعة",
        "انتظار",
        "متأخر",
    ]):
        return (
            "Workflow monitoring is available.\n"
            "Pending approval analysis will be connected to the academic workflow engine."
        )

    # Default executive response
    return (
        "I can help you with:\n\n"
        "- Student statistics\n"
        "- Academic theses\n"
        "- Defense committees\n"
        "- Executive reports\n"
        "- Academic workflow follow-up"
    )
