import re

COMMON_NAMES = {
    "محمد": "Mohamed", "أحمد": "Ahmed", "احمد": "Ahmed", "محمود": "Mahmoud",
    "عبد": "Abdel", "الباسط": "Baset", "خلاف": "Khalaf", "علي": "Ali",
    "حسن": "Hassan", "حسين": "Hussein", "منى": "Mona", "مصطفى": "Mostafa",
    "إبراهيم": "Ibrahim", "ابراهيم": "Ibrahim", "خالد": "Khaled", "عمر": "Omar",
    "عمرو": "Amr", "يوسف": "Youssef", "ياسر": "Yasser", "طارق": "Tarek",
    "هبة": "Heba", "سارة": "Sara", "مريم": "Mariam", "فاطمة": "Fatma",
    "عبدالله": "Abdullah", "عبدالرحمن": "Abdelrahman", "عبدالعزيز": "Abdelaziz",
}
CHARACTERS = {
    "ا": "a", "أ": "a", "إ": "e", "آ": "a", "ب": "b", "ت": "t", "ث": "th",
    "ج": "g", "ح": "h", "خ": "kh", "د": "d", "ذ": "z", "ر": "r", "ز": "z",
    "س": "s", "ش": "sh", "ص": "s", "ض": "d", "ط": "t", "ظ": "z", "ع": "a",
    "غ": "gh", "ف": "f", "ق": "q", "ك": "k", "ل": "l", "م": "m", "ن": "n",
    "ه": "h", "ة": "a", "و": "w", "ؤ": "o", "ي": "y", "ى": "a", "ئ": "e", "ء": "",
}

def transliterate_arabic_name(value):
    """Create an editable Latin-script initial value; never replace reviewed names."""
    parts = re.findall(r"[\u0600-\u06ff]+|[^\u0600-\u06ff]+", (value or "").strip())
    output = []
    for part in parts:
        if part in COMMON_NAMES:
            output.append(COMMON_NAMES[part])
        elif re.search(r"[\u0600-\u06ff]", part):
            output.append("".join(CHARACTERS.get(char, "") for char in part).capitalize())
        else:
            output.append(part)
    return re.sub(r"\s+", " ", "".join(output)).strip()
