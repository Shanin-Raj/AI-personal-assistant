"""
assistant/core.py
──────────────────
S.H.A.N.I.N. Mark II — Main assistant loop.

Flow per turn:
    1. Press Enter  (press-to-talk trigger)
    2. Record 7 s from internal mic via audio.listen()
    3. Log user turn to SQLite
    4. Classify intent via Gemini (intent.get_intent)
    5. Dispatch to tool
    6. Log assistant response to SQLite
    7. Repeat until exit phrase heard
"""

from assistant.audio  import speak, listen
from assistant.intent import get_intent
from assistant.tools  import search, news, notes
import memory.db as db

EXIT_PHRASES = {"exit", "quit", "goodbye", "stop", "shut down", "bye", "close"}


def _dispatch(intent_data: dict, gemini_key: str, news_key: str) -> str:
    """Route intent to the correct tool. Returns assistant's spoken action."""
    intent = intent_data.get("intent", "unknown")
    query  = intent_data.get("query", "")

    if intent == "get_news":
        news.get_news_summary(gemini_key, news_key)
        return "news summary delivered"

    elif intent == "search":
        search.structured_search(query, gemini_key)
        return f"searched Wikipedia for '{query}'"

    elif intent == "fast_search":
        search.fast_search(query, gemini_key)
        return f"fast search answer for '{query}'"

    elif intent == "add_note":
        speak("What should the note say?")
        input("\n[Press Enter to speak your note]")
        note_text = listen()
        if note_text:
            notes.add_note(note_text)
            return f"note saved: '{note_text}'"
        else:
            speak("I didn't catch that. Note not saved.")
            return "add_note: no speech detected"

    elif intent == "view_notes":
        notes.view_notes()
        return "notes read back"

    else:
        msg = "Sorry, I couldn't understand that. Please try again."
        print(f"[Core] Unknown intent: {intent_data}")
        speak(msg)
        return "unknown intent"


def run_loop(gemini_key: str, news_key: str) -> None:
    """
    Main press-to-talk conversation loop.
    Runs until the user says an exit phrase.
    """
    try:
        speak("S.H.A.N.I.N. Mark II online. Press Enter to speak.")
    except Exception as e:
        print(f"[Core] TTS warning (non-fatal): {e}")
        print("[Core] S.H.A.N.I.N. Mark II online. Press Enter to speak.")

    while True:
        try:
            input("\n[Press Enter to speak — or Ctrl+C to force quit]\n")
        except KeyboardInterrupt:
            speak("Force quit detected. Goodbye.")
            break

        # ── Listen ────────────────────────────────────────────────────────────
        try:
            user_text = listen()
        except Exception as e:
            print(f"[Core] Audio error: {e}")
            print("[Core] Could not record audio — check microphone. Press Enter to retry.")
            continue

        if not user_text:
            print("[Core] Nothing heard — try again.")
            try:
                speak("I didn't catch that. Please press Enter and try again.")
            except Exception:
                print("[Core] I didn't catch that. Please press Enter and try again.")
            continue

        print(f"[Core] You said: '{user_text}'")
        db.log_turn("user", user_text)

        # ── Exit check ────────────────────────────────────────────────────────
        if any(phrase in user_text for phrase in EXIT_PHRASES):
            farewell = "Goodbye. S.H.A.N.I.N. shutting down."
            try:
                speak(farewell)
            except Exception:
                print(f"[Core] {farewell}")
            db.log_turn("assistant", farewell)
            break

        # ── Classify & dispatch ───────────────────────────────────────────────
        intent_data = get_intent(user_text, gemini_key)
        action_desc = _dispatch(intent_data, gemini_key, news_key)
        db.log_turn("assistant", action_desc)
