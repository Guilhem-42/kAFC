import os
import httpx
from dotenv import load_dotenv

load_dotenv()

SPEECHMATICS_API_KEY = os.getenv("SPEECHMATICS_API_KEY")
TTS_URL = "https://mp.speechmatics.com/v1/tts"

# Voix disponibles par langue dans Speechmatics Flow
# Format : code_langue → voice_id
VOICE_MAP = {
    "ar": "Arabic Female",
    "bg": "Bulgarian Male",
    "hr": "Croatian Male",
    "cs": "Czech Female",
    "da": "Danish Female",
    "nl": "Dutch Female",
    "en": "English (British) Female",
    "fi": "Finnish Female",
    "fr": "French Male",
    "de": "German Male",
    "el": "Greek Male",
    "hi": "Hindi Female",
    "hu": "Hungarian Female",
    "id": "Indonesian Female",
    "it": "Italian Female",
    "ja": "Japanese Female",
    "ko": "Korean Female",
    "ms": "English/Malay Female",
    "zh": "English/Mandarin Male",
    "no": "Norwegian Male",
    "pl": "Polish Male",
    "pt": "Portuguese Male",
    "ro": "Romanian Female",
    "ru": "Russian Male",
    "sk": "Slovak Male",
    "es": "English/Spanish Male",
    "sv": "Swedish Female",
    "ta": "English/Tamil Female",
    "th": "Thai Female",
    "tr": "Turkish Female",
    "uk": "Ukrainian Female",
    "vi": "Vietnamese Female",
}

# Voix par défaut pour le poussin (réponses en fr/en)
DEFAULT_VOICE = "French Male"


async def synthesize(text: str, lang_code: str = "fr") -> bytes:
    """
    Synthétise du texte en audio via Speechmatics TTS.
    Retourne les bytes audio (MP3).
    """
    voice = VOICE_MAP.get(lang_code, DEFAULT_VOICE)

    async with httpx.AsyncClient() as client:
        response = await client.post(
            TTS_URL,
            headers={
                "Authorization": f"Bearer {SPEECHMATICS_API_KEY}",
                "Content-Type": "application/json",
            },
            json={
                "input": text,
                "voice": voice,
                "output_format": {
                    "type": "mp3",
                    "sample_rate": 22050,
                },
            },
            timeout=15.0,
        )
        response.raise_for_status()
        return response.content
