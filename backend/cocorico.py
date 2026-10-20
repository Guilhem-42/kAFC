import random

# Table complète des Cocoricos — 32 langues Speechmatics Flow
COCORICO_TABLE = [
    {"lang": "Arabic",    "code": "ar", "text": "كوكو ريكو",       "phonetic": "Kuku riku"},
    {"lang": "Bulgarian", "code": "bg", "text": "Кукуригу",         "phonetic": "Kukurigu"},
    {"lang": "Croatian",  "code": "hr", "text": "Kukuriku",         "phonetic": "Kukuriku"},
    {"lang": "Czech",     "code": "cs", "text": "Kykyryký",         "phonetic": "Kikiriki"},
    {"lang": "Danish",    "code": "da", "text": "Kykkeliky",        "phonetic": "Keukeliku"},
    {"lang": "Dutch",     "code": "nl", "text": "Kukeleku",         "phonetic": "Koukelkou"},
    {"lang": "English",   "code": "en", "text": "Cock-a-doodle-doo","phonetic": "Kok-a-doudel-dou"},
    {"lang": "Finnish",   "code": "fi", "text": "Kukkokiekuu",      "phonetic": "Koukkokiékou"},
    {"lang": "French",    "code": "fr", "text": "Cocorico",         "phonetic": "Cocorico"},
    {"lang": "German",    "code": "de", "text": "Kikeriki",         "phonetic": "Kikeriki"},
    {"lang": "Greek",     "code": "el", "text": "Κικιρίκου",        "phonetic": "Kikiriku"},
    {"lang": "Hindi",     "code": "hi", "text": "कुकड़ूकूं",        "phonetic": "Kukadookoo"},
    {"lang": "Hungarian", "code": "hu", "text": "Kukurikú",         "phonetic": "Koukourikou"},
    {"lang": "Indonesian","code": "id", "text": "Kukuruyuk",        "phonetic": "Koukourouyouk"},
    {"lang": "Italian",   "code": "it", "text": "Chicchirichì",     "phonetic": "Kikiriki"},
    {"lang": "Japanese",  "code": "ja", "text": "コケコッコー",      "phonetic": "Kokekokkō"},
    {"lang": "Korean",    "code": "ko", "text": "꼬끼오",            "phonetic": "Kkokki-o"},
    {"lang": "Malay",     "code": "ms", "text": "Kukuruyuk",        "phonetic": "Koukourouyouk"},
    {"lang": "Mandarin",  "code": "zh", "text": "喔喔",              "phonetic": "Wō wō"},
    {"lang": "Norwegian", "code": "no", "text": "Kykkeliky",        "phonetic": "Keukeliku"},
    {"lang": "Polish",    "code": "pl", "text": "Kukuryku",         "phonetic": "Koukouritykou"},
    {"lang": "Portuguese","code": "pt", "text": "Cocorocó",         "phonetic": "Cocorocó"},
    {"lang": "Romanian",  "code": "ro", "text": "Cucurigu",         "phonetic": "Tsoukourigou"},
    {"lang": "Russian",   "code": "ru", "text": "Кукареку",         "phonetic": "Kukaryeku"},
    {"lang": "Slovak",    "code": "sk", "text": "Kykyriký",         "phonetic": "Kikiriki"},
    {"lang": "Spanish",   "code": "es", "text": "Quiquiriquí",      "phonetic": "Kikiriqi"},
    {"lang": "Swedish",   "code": "sv", "text": "Kuckeliku",        "phonetic": "Koukeliku"},
    {"lang": "Tamil",     "code": "ta", "text": "கொக்கரக்கோ",      "phonetic": "Kokkarakko"},
    {"lang": "Thai",      "code": "th", "text": "เอ้กอีเอ้ก",       "phonetic": "Ék-i-ék"},
    {"lang": "Turkish",   "code": "tr", "text": "Üürüüü",           "phonetic": "Uuruuu"},
    {"lang": "Ukrainian", "code": "uk", "text": "Кукуріку",         "phonetic": "Kukuriku"},
    {"lang": "Vietnamese","code": "vi", "text": "Ò ó o",            "phonetic": "O-o-o"},
]

def pick_random_cocorico(exclude_lang: str | None = None) -> dict:
    """
    Tire un Cocorico aléatoire dans la table.
    On peut exclure la langue détectée pour éviter de répéter
    la même que celle de l'utilisateur (optionnel).
    """
    pool = [c for c in COCORICO_TABLE if c["code"] != exclude_lang]
    return random.choice(pool)
