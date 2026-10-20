#!/usr/bin/env python3
"""
kAFC — Setup checker
Vérifie que toutes les clés API sont présentes dans .env
et teste la connectivité avec chaque service.

Usage :
    python check_setup.py
"""

import os
import sys
import asyncio
import httpx
from dotenv import load_dotenv

load_dotenv()

# ─────────────────────────────────────────────
# Configuration des variables requises
# ─────────────────────────────────────────────

REQUIRED = {
    "SPEECHMATICS_API_KEY": {
        "label": "Speechmatics API Key",
        "how":   "https://portal.speechmatics.com/ → API Keys → Create API Key",
        "test":  "speechmatics",
    },
    "ANTHROPIC_API_KEY": {
        "label": "Anthropic (Claude) API Key",
        "how":   "https://console.anthropic.com/ → API Keys → Create Key",
        "test":  "anthropic",
    },
}

# ─────────────────────────────────────────────
# Helpers d'affichage
# ─────────────────────────────────────────────

GREEN  = "\033[92m"
RED    = "\033[91m"
YELLOW = "\033[93m"
RESET  = "\033[0m"
BOLD   = "\033[1m"

def ok(msg):    print(f"  {GREEN}✔{RESET}  {msg}")
def fail(msg):  print(f"  {RED}✘{RESET}  {msg}")
def warn(msg):  print(f"  {YELLOW}⚠{RESET}  {msg}")
def title(msg): print(f"\n{BOLD}{msg}{RESET}")

# ─────────────────────────────────────────────
# Tests de connectivité
# ─────────────────────────────────────────────

async def test_speechmatics(key: str) -> bool:
    """
    Teste la clé Speechmatics via GET /v2/jobs/ — endpoint REST simple
    qui confirme qu'une clé est valide sans créer de ressource.
    """
    try:
        async with httpx.AsyncClient(timeout=8) as client:
            r = await client.get(
                "https://asr.api.speechmatics.com/v2/jobs/",
                headers={"Authorization": f"Bearer {key}"},
            )
            if r.status_code in (200, 404):
                ok("Speechmatics API Key valide")
                return True
            elif r.status_code == 401:
                fail("Speechmatics : clé invalide ou expirée (401)")
            elif r.status_code == 403:
                fail("Speechmatics : accès refusé — vérifier les permissions (403)")
            else:
                warn(f"Speechmatics : réponse inattendue ({r.status_code}) — {r.text[:120]}")
    except httpx.ConnectError:
        fail("Speechmatics : impossible de joindre l'API (réseau ?)")
    except Exception as e:
        fail(f"Speechmatics : erreur inattendue — {e}")
    return False


async def test_anthropic(key: str) -> bool:
    """
    Teste la clé Anthropic avec un appel minimal.
    Vérifie aussi le format de la clé avant l'appel.
    """
    # Vérification du format — toute clé Anthropic commence par "sk-ant-"
    if not key.startswith("sk-ant-"):
        fail(
            f"Anthropic : format de clé incorrect (commence par '{key[:8]}…' "
            f"au lieu de 'sk-ant-…')\n"
            f"       → Vérifier le copier-coller dans .env, sans espace ni caractère parasite"
        )
        return False

    try:
        async with httpx.AsyncClient(timeout=10) as client:
            r = await client.post(
                "https://api.anthropic.com/v1/messages",
                headers={
                    "x-api-key": key,
                    "anthropic-version": "2023-06-01",
                    "content-type": "application/json",
                },
                json={
                    "model": "claude-haiku-4-5-20251001",
                    "max_tokens": 10,
                    "messages": [{"role": "user", "content": "Cocorico ?"}],
                },
            )
            if r.status_code == 200:
                ok("Anthropic API Key valide")
                return True
            elif r.status_code == 401:
                fail("Anthropic : clé invalide ou expirée (401) — regénérer une clé sur console.anthropic.com")
            elif r.status_code == 403:
                fail("Anthropic : accès refusé — vérifier les permissions de la clé (403)")
            else:
                warn(f"Anthropic : réponse inattendue ({r.status_code}) — {r.text[:120]}")
    except httpx.ConnectError:
        fail("Anthropic : impossible de joindre l'API (réseau ?)")
    except Exception as e:
        fail(f"Anthropic : erreur inattendue — {e}")
    return False


TESTERS = {
    "speechmatics": test_speechmatics,
    "anthropic":    test_anthropic,
}

# ─────────────────────────────────────────────
# Main
# ─────────────────────────────────────────────

async def main():
    print(f"\n{BOLD}{'='*50}{RESET}")
    print(f"{BOLD}  kAFC — Setup Checker{RESET}")
    print(f"{BOLD}{'='*50}{RESET}")

    # 1. Vérifier la présence du fichier .env
    title("1. Fichier .env")
    env_path = os.path.join(os.path.dirname(__file__), ".env")
    if os.path.exists(env_path):
        ok(".env trouvé")
    else:
        fail(".env introuvable — copier .env.example en .env et renseigner les clés")
        print(f"\n     {YELLOW}cp .env.example .env{RESET}\n")
        sys.exit(1)

    # 2. Vérifier la présence de chaque variable
    title("2. Variables d'environnement")
    missing = []
    found   = {}

    for var, meta in REQUIRED.items():
        value = os.getenv(var, "").strip()
        if not value or value.startswith("your_"):
            fail(f"{var} manquant")
            print(f"       → {meta['label']}")
            print(f"       → Obtenir ici : {meta['how']}")
            missing.append(var)
        else:
            masked = value[:6] + "…" + value[-4:]
            ok(f"{var} présent ({masked})")
            found[var] = value

    if missing:
        print(f"\n  {RED}→ {len(missing)} variable(s) manquante(s). Compléter .env avant de continuer.{RESET}\n")
        sys.exit(1)

    # 3. Tester la connectivité avec chaque service
    title("3. Test de connectivité API")
    results = {}

    for var, meta in REQUIRED.items():
        tester = TESTERS.get(meta["test"])
        if tester:
            results[var] = await tester(found[var])

    # 4. Résumé
    title("4. Résumé")
    all_ok = all(results.values())

    if all_ok:
        print(f"\n  {GREEN}{BOLD}✔ Tout est en ordre — vous pouvez lancer kAFC !{RESET}")
        print(f"\n  Backend  : {BOLD}uvicorn main:app --reload --port 8000{RESET}")
        print(f"  Frontend : {BOLD}npm run dev{RESET} (dans /frontend)\n")
    else:
        failed = [var for var, ok_ in results.items() if not ok_]
        print(f"\n  {RED}✘ {len(failed)} service(s) inaccessible(s) : {', '.join(failed)}{RESET}")
        print(f"  Vérifier les clés et la connexion réseau.\n")
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())
