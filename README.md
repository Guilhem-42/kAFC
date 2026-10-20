# kAFC — Kute Artificial Friend Chicken
> *He'll never solve your problem. But he'll fail to do so in Mandarin.*

Agent conversationnel vocal multilingue et hilarant, développé pour le hackathon Voice AI.

*Hilarious multilingual voice agent, built for the Voice AI hackathon (Activate Your Voice, Feb. 2026).*

---

## Architecture

```
Browser mic → WebSocket → FastAPI backend → Speechmatics STT
                                          → Claude API
                                          → Speechmatics TTS
                                          → WebSocket retour
                                              → Séquences vidéo marionnette
                                              → Audio poussin
```

---

## Stack

| Composant | Techno |
|---|---|
| Frontend | React + Vite |
| Backend | Python / FastAPI |
| STT + Language ID | Speechmatics Flow |
| LLM | Claude API (claude-sonnet-4-6) |
| TTS | Speechmatics TTS |
| Cocorico | Tirage aléatoire backend (32 langues) |

---

## Installation

### Prérequis
- Node.js 18+
- Python 3.11+
- Clés API : Speechmatics + Anthropic

### Backend

```bash
cd backend
python -m venv .venv
source .venv/bin/activate      # Windows : .venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env           # puis renseigner les clés
uvicorn main:app --reload --port 8000
```

### Frontend

```bash
cd frontend
npm install
npm run dev                    # → http://localhost:5173
```

---

## Variables d'environnement

Copier `backend/.env.example` en `backend/.env` :

```
SPEECHMATICS_API_KEY=your_key_here
ANTHROPIC_API_KEY=your_key_here
```

---

## Séquences vidéo marionnette

Placer les fichiers MP4 dans `frontend/src/assets/videos/` :

| Fichier | Description |
|---|---|
| `intro.mp4` | Entrée dans le champ |
| `waiting_a.mp4` | Attente — variante A (loop) |
| `waiting_b.mp4` | Attente — variante B (loop) |
| `receiving.mp4` | Réception de la question |
| `talking.mp4` | Parole (loop pendant TTS) |
| `dance.mp4` | La grande danse absurde |
| `spin.mp4` | Tourne sur elle-même |
| `exit.mp4` | La main attrape le poussin par le cou |

> ⚠️ Les MP4 sont gitignorés par défaut. Utiliser Git LFS ou les distribuer manuellement.

---

## Logique Cocorico

Le backend tire aléatoirement un Cocorico dans une table de 32 langues (voir `backend/cocorico.py`).
Le LLM n'a pas à choisir — il reçoit le Cocorico sélectionné dans son contexte et l'annonce.

---

*kAFC — Hackathon Voice AI*
