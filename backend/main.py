import asyncio
import base64
import json
import os
import websockets

from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

from cocorico import pick_random_cocorico
from claude import generate_response
from tts import synthesize
from speechmatics import get_jwt_token, build_rt_config, SPEECHMATICS_RT_URL

load_dotenv()

app = FastAPI(title="kAFC Backend")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Vite dev server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
async def health():
    return {"status": "ok", "service": "kAFC"}


@app.websocket("/ws/session")
async def kafc_session(client_ws: WebSocket):
    """
    WebSocket principal entre le browser et le backend.

    Protocole messages backend → frontend :
      { "type": "state",   "value": "listening"|"receiving"|"talking"|"dance"|"exit" }
      { "type": "transcript", "text": "...", "lang": "fr" }
      { "type": "cocorico", "lang": "Japanese", "text": "コケコッコー", "phonetic": "Kokekokkō" }
      { "type": "audio",   "data": "<base64 mp3>" }
      { "type": "error",   "message": "..." }
    """
    await client_ws.accept()
    print("Client connecté")

    try:
        # 1. Intro — signale au frontend d'afficher la séquence d'entrée
        await send(client_ws, {"type": "state", "value": "intro"})
        await asyncio.sleep(2.5)

        # 2. Obtenir un JWT Speechmatics temps réel
        jwt = await get_jwt_token()

        # 3. Ouvrir la connexion WebSocket vers Speechmatics RT
        sm_url = f"{SPEECHMATICS_RT_URL}?jwt={jwt}"

        async with websockets.connect(sm_url) as sm_ws:

            # Envoyer la config de reconnaissance
            config = build_rt_config(language="auto")
            await sm_ws.send(json.dumps(config))

            # Attendre RecognitionStarted
            resp = json.loads(await sm_ws.recv())
            if resp.get("message") != "RecognitionStarted":
                await send(client_ws, {"type": "error", "message": "Speechmatics init failed"})
                return

            # Signaler au frontend : en attente de parole
            await send(client_ws, {"type": "state", "value": "waiting"})

            transcript_text = ""
            detected_lang = "fr"
            audio_buffer = bytearray()

            async def receive_from_speechmatics():
                """Écoute les messages Speechmatics et extrait la transcription finale."""
                nonlocal transcript_text, detected_lang
                async for raw in sm_ws:
                    msg = json.loads(raw)

                    if msg.get("message") == "AddTranscript":
                        for result in msg.get("results", []):
                            if result.get("type") == "word":
                                alts = result.get("alternatives", [])
                                if alts:
                                    transcript_text += alts[0].get("content", "") + " "
                                    if "language" in alts[0]:
                                        detected_lang = alts[0]["language"]

                    elif msg.get("message") == "EndOfTranscript":
                        break

            async def forward_audio_from_client():
                """Reçoit l'audio du browser et le transfère à Speechmatics."""
                try:
                    while True:
                        data = await client_ws.receive_bytes()
                        audio_buffer.extend(data)
                        await sm_ws.send(data)
                except WebSocketDisconnect:
                    pass
                finally:
                    # Signaler la fin de l'audio à Speechmatics
                    await sm_ws.send(json.dumps({"message": "EndOfStream", "last_seq_no": 0}))

            # Lancer les deux tâches en parallèle
            await asyncio.gather(
                forward_audio_from_client(),
                receive_from_speechmatics(),
            )

            # 4. Transcription reçue
            transcript_text = transcript_text.strip()
            await send(client_ws, {
                "type": "transcript",
                "text": transcript_text,
                "lang": detected_lang,
            })
            await send(client_ws, {"type": "state", "value": "receiving"})

            # 5. Tirage aléatoire du Cocorico (backend, pas LLM)
            cocorico = pick_random_cocorico(exclude_lang=detected_lang)
            await send(client_ws, {
                "type": "cocorico",
                "lang": cocorico["lang"],
                "text": cocorico["text"],
                "phonetic": cocorico["phonetic"],
            })

            # 6. Générer la réponse via Claude
            response_text = await generate_response(transcript_text, cocorico)

            # 7. Synthèse vocale
            await send(client_ws, {"type": "state", "value": "talking"})
            audio_bytes = await synthesize(response_text, lang_code="fr")
            audio_b64 = base64.b64encode(audio_bytes).decode("utf-8")
            await send(client_ws, {"type": "audio", "data": audio_b64})

            # 8. Danse !
            await send(client_ws, {"type": "state", "value": "dance"})
            await asyncio.sleep(5)

            # 9. Exit — la main attrape le poussin
            await send(client_ws, {"type": "state", "value": "exit"})
            await asyncio.sleep(2.5)

    except WebSocketDisconnect:
        print("Client déconnecté")
    except Exception as e:
        print(f"Erreur session : {e}")
        try:
            await send(client_ws, {"type": "error", "message": str(e)})
        except Exception:
            pass


async def send(ws: WebSocket, data: dict):
    await ws.send_text(json.dumps(data))
