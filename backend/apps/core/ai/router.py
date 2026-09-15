"""Deterministic bilingual intent routing for academic intelligence."""

INTENT_RULES = (
    (
        "analytics",
        (
            "academic kpi",
            "executive summary",
            "department statistics",
            "statistics",
            "kpi",
            "ملخص تنفيذي",
            "مؤشرات",
            "إحصائيات الأقسام",
            "احصائيات الأقسام",
            "تحليلات",
        ),
    ),
    (
        "workflow",
        (
            "pending approval",
            "pending approvals",
            "waiting review",
            "workflow",
            "bottleneck",
            "approval",
            "اعتماد",
            "موافقة",
            "مراجعة",
            "اختناق",
            "قراري",
            "قرار",
        ),
    ),
    (
        "committees",
        ("committee", "committees", "defense", "defenses", "لجنة", "لجان", "مناقشة", "مناقشات"),
    ),
    ("theses", ("thesis", "theses", "رسالة", "رسائل", "أطروحة", "اطروحة")),
    ("students", ("student", "students", "طالب", "طلاب", "university id", "رقم جامعي")),
)


def detect_intent(question):
    text = (question or "").casefold()
    for intent, keywords in INTENT_RULES:
        if any(keyword in text for keyword in keywords):
            return intent
    return "general"


def general_ai_answer(question, language="en"):
    if language == "ar":
        return (
            "يمكنني تحليل الطلاب والرسائل واللجان والمناقشات ومسارات الاعتماد "
            "والمؤشرات الأكاديمية وفق صلاحيات حسابك."
        )
    return (
        "I can analyze students, theses, committees, defenses, approval workflows, "
        "and academic KPIs within your account permissions."
    )
