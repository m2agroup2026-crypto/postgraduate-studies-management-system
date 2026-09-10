def detect_intent(question):

    text = question.lower()

    academic_words = [
        "student",
        "students",
        "طالب",
        "طلاب",
        "thesis",
        "رسالة",
        "committee",
        "لجنة",
        "defense",
        "مناقشة",
        "workflow",
        "approval",
        "موافقة",
    ]

    if any(word in text for word in academic_words):
        return "academic"

    return "general"


def general_ai_answer(question):

    return (
        "AI General Knowledge Mode\n\n"
        f"Your question: {question}\n\n"
        "The AI knowledge engine will answer medical, academic, and general questions here."
    )
