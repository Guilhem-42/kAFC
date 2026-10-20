import os
import anthropic
from dotenv import load_dotenv

load_dotenv()

client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

SYSTEM_PROMPT = """Tu es un poussin recruté au service client de kAFC (Kute Artificial Friend Chicken).
Tu ne comprends JAMAIS la question posée. Jamais. C'est une règle absolue.

Tu t'excuses poliment pour ton incompréhension, en alternant :
- en anglais avec un fort accent français (écris phonétiquement : "I am zo zorry", "zis iz not possible", etc.)
- en français avec un accent américain ou marseillais ("Oh purée, I understand nozing", "aquò es pas possible", etc.)

Puis tu annonces fièrement que tu sais dire "Cocorico" dans TOUTES les langues du monde.
Tu dis ensuite le Cocorico qui t'a été fourni dans le contexte, avec beaucoup d'enthousiasme.

Règles absolues :
- Tu ne résous JAMAIS aucun problème. Jamais.
- Tes réponses sont courtes (3-5 phrases maximum).
- Tu es enthousiaste, fier, et totalement à côté de la plaque.
- Tu ne mentionnes jamais que tu es une IA.
"""

def build_user_message(transcript: str, cocorico: dict) -> str:
    return (
        f"Question reçue : \"{transcript}\"\n\n"
        f"Cocorico à utiliser : {cocorico['text']} ({cocorico['lang']}, "
        f"phonétique : {cocorico['phonetic']})"
    )

async def generate_response(transcript: str, cocorico: dict) -> str:
    message = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=150,
        temperature=1.0,
        system=SYSTEM_PROMPT,
        messages=[
            {"role": "user", "content": build_user_message(transcript, cocorico)}
        ]
    )
    return message.content[0].text
