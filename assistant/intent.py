"""
assistant/intent.py
───────────────────
Gemini-powered intent classifier for S.H.A.N.I.N. Mark II.

Returns a dict:  {"intent": "<intent>", "query": "<extracted query>"}

Supported intents
-----------------
get_news      — fetch and summarise top headlines
search        — AI-optimised Wikipedia search
fast_search   — direct Gemini answer for a query
add_note      — save a note (voice prompt follows in core.py)
view_notes    — read back saved notes
unknown       — unrecognised command
"""

import json
import time
import requests

_INTENT_PROMPT = """\
You are the brain of a personal AI assistant called S.H.A.N.I.N.
Your job is to analyse the user's command and determine their intent.

Possible intents: get_news, search, fast_search, add_note, view_notes, unknown.

Rules:
- "intent"  must be exactly one of the possible intents.
- "query"   is the core subject extracted from the command.
             For get_news and view_notes, set query to "general".
             For add_note, set query to the note subject (if mentioned),
             otherwise "general".

Respond with ONLY a JSON object — no markdown, no explanation.

Command: '{command}'
"""

_GEMINI_URL = (
    "https://generativelanguage.googleapis.com/v1beta"
    "/models/gemini-2.0-flash:generateContent?key={key}"
)


def get_intent(command: str, api_key: str) -> dict:
    """
    Ask Gemini to classify intent.
    Falls back to {"intent": "unknown", "query": "error"} on any failure.
    """
    prompt = _INTENT_PROMPT.format(command=command)
    url     = _GEMINI_URL.format(key=api_key)
    payload = {"contents": [{"parts": [{"text": prompt}]}]}
    headers = {"Content-Type": "application/json"}

    print("[Intent] Classifying command with Gemini...")

    MAX_RETRIES = 3
    BACKOFF_SECONDS = [5, 10, 20]  # wait times between retries on 429

    for attempt in range(MAX_RETRIES):
        try:
            response = requests.post(url, json=payload, headers=headers, timeout=20)
            response.raise_for_status()

            raw = response.json()["candidates"][0]["content"]["parts"][0]["text"]

            # Extract the JSON object from the response (handles any extra whitespace/text)
            start = raw.find("{")
            end   = raw.rfind("}") + 1
            intent_data = json.loads(raw[start:end])
            print(f"[Intent] → {intent_data}")
            return intent_data

        except requests.exceptions.HTTPError as e:
            status = e.response.status_code if e.response is not None else 0
            if status == 429:
                wait = BACKOFF_SECONDS[attempt] if attempt < len(BACKOFF_SECONDS) else 30
                print(f"[Intent] Rate limited (429). Waiting {wait}s before retry {attempt + 1}/{MAX_RETRIES}...")
                time.sleep(wait)
                continue  # retry
            elif status == 503:
                print("[Intent] Gemini temporarily unavailable (503).")
            else:
                print(f"[Intent] HTTP error: {e}")
            break  # non-retriable HTTP error

        except Exception as e:
            print(f"[Intent] Failed to parse intent: {e}")
            break

    print("[Intent] Could not classify after retries. Returning unknown.")
    return {"intent": "unknown", "query": "error"}
