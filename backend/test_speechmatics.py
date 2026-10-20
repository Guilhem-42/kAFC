import os
import asyncio
import httpx
from dotenv import load_dotenv

load_dotenv()

SPEECHMATICS_API_KEY = os.getenv("SPEECHMATICS_API_KEY")
SPEECHMATICS_RT_URL = "wss://eu2.rt.speechmatics.com/v2"

# Langues supportées par Speechmatics Flow
SUPPORTED_LANGUAGES = [
    "ar","bg","hr","cs","da","nl","en","fi","fr","de",
    "el","hi","hu","id","it","ja","ko","ms","zh","no",
    "pl","pt","ro","ru","sk","es","sv","ta","th","tr","uk","vi"
]

def build_rt_config(language: str = "auto") -> dict:
    """
    Config pour la reconnaissance temps réel Speechmatics.
    'auto' active la détection automatique de langue.
    """
    config = {
        "type": "StartRecognition",
        "transcription_config": {
            "operating_point": "enhanced",
            "enable_partials": False,
            "max_delay": 2.0,
        },
        "audio_format": {
            "type": "raw",
            "encoding": "pcm_f32le",
            "sample_rate": 16000,
        },
    }

    if language == "auto":
        config["transcription_config"]["language"] = "auto"
    else:
        config["transcription_config"]["language"] = language

    return config


async def get_jwt_token() -> str:
    """
    Obtient un JWT de courte durée pour la connexion WebSocket temps réel.
    """
    async with httpx.AsyncClient() as client:
        response = await client.post(
            "https://mp.speechmatics.com/v1/api_keys?type=rt",
            headers={
                "Authorization": f"Bearer {SPEECHMATICS_API_KEY}",
                "Content-Type": "application/json",
            },
            json={"ttl": 60},
        )
        response.raise_for_status()
        return response.json()["key_value"]
