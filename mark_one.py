# Import all necessary libraries
import argparse
import requests 
import os
from dotenv import load_dotenv
import wikipediaapi
import speech_recognition as sr # NEW: Import speech recognition

# Load environment variables from the .env file
load_dotenv()

# --- Feature Functions ---
# (These functions: fast_search and structured_search remain the same)

def fast_search(query, api_key):
    """
    MODE 1: Uses the Gemini AI to directly answer a user's query.
    """
    print(f"-> Asking Gemini for a quick summary of: '{query}'...")
    prompt = (
        f"Please provide a concise, three-sentence summary that directly answers the following query.\n"
        f"Query: '{query}'"
    )
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash-latest:generateContent?key={api_key}"
    payload = {"contents": [{"parts": [{"text": prompt}]}]}
    headers = {'Content-Type': 'application/json'}

    try:
        response = requests.post(url, json=payload, headers=headers, timeout=20)
        response.raise_for_status()
        data = response.json()
        summary = data['candidates'][0]['content']['parts'][0]['text'].strip()
        print(f"\n--- AI Generated Summary ---\n{summary}")
    except Exception as e:
        print(f"An error occurred: {e}")


def structured_search(query, api_key):
    """
    MODE 2: Uses AI to optimize a search term and then searches Wikipedia.
    """
    print(f"-> Optimizing search term with AI...")
    prompt = (
        f"Based on the following user query, what is the best possible search term for Wikipedia? "
        f"Respond with only the ideal search term and nothing else.\n"
        f"Query: '{query}'"
    )
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash-latest:generateContent?key={api_key}"
    payload = {"contents": [{"parts": [{"text": prompt}]}]}
    headers = {'Content-Type': 'application/json'}

    try:
        response = requests.post(url, json=payload, headers=headers, timeout=20)
        response.raise_for_status()
        data = response.json()
        optimized_term = data['candidates'][0]['content']['parts'][0]['text'].strip()
        print(f"-> AI suggested search term: '{optimized_term}'")
    except Exception as e:
        print(f"An error occurred during optimization: {e}")
        print("-> Using original query for search.")
        optimized_term = query

    print(f"-> Searching Wikipedia for '{optimized_term}'...")
    wiki_wiki = wikipediaapi.Wikipedia(user_agent='Mark-I-Assistant/1.0', language='en')
    page = wiki_wiki.page(optimized_term)

    if not page.exists():
        print(f"Sorry, I could not find a Wikipedia page for '{optimized_term}'.")
        return

    print(f"\n--- Result for: {page.title} ---")
    summary_sentences = page.summary.split('.')
    print(". ".join(summary_sentences[:3]) + ".")

# ---  Voice Command Functions ---

def listen_for_command():
    """
    Listens for a command from the microphone and returns the recognized text.
    """
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Calibrating microphone...")
        r.adjust_for_ambient_noise(source, duration=1)
        print("Awaiting your command...")
        try:
            audio = r.listen(source, timeout=5, phrase_time_limit=10)
            print("Recognizing...")
            text = r.recognize_google(audio)
            print(f"-> You said: '{text}'")
            return text.lower() # Return text in lowercase for easier processing
        except sr.WaitTimeoutError:
            print("Timeout: No command was heard.")
            return None
        except sr.UnknownValueError:
            print("Sorry, I could not understand the audio.")
            return None
        except sr.RequestError as e:
            print(f"API Error: {e}")
            return None

def process_voice_command(command, api_key):
    """
    Analyzes the recognized text and calls the appropriate function.
    """
    if command is None:
        return

    # A simple way to check for keywords in the command
    if "fast search" in command:
        # We remove the keywords to get the actual query
        query = command.replace("fast search", "").strip()
        fast_search(query, api_key)
    elif "search" in command:
        query = command.replace("search", "").strip()
        structured_search(query, api_key)
    else:
        print("Sorry, I didn't recognize that command. Please say 'search' or 'fast search'.")


# --- Main Controller ---
def main():
    parser = argparse.ArgumentParser(description="Mark I: Your Personal AI Assistant.")
    group = parser.add_mutually_exclusive_group(required=True)
    
    group.add_argument('--search', type=str, nargs='+', help="Perform a structured search.")
    group.add_argument('--fast-search', type=str, nargs='+', help="Get a quick AI summary.")
    # NEW: Add the --listen command. 'action='store_true'' means it doesn't need a value.
    group.add_argument('--listen', action='store_true', help="Listen for a voice command.")

    args = parser.parse_args()
    
    gemini_api_key = os.getenv("GEMINI_API_KEY")
    if not gemini_api_key:
        print("Error: GEMINI_API_KEY not found in .env file.")
        return

    # --- Command Dispatcher ---
    if args.search:
        query = " ".join(args.search)
        structured_search(query, gemini_api_key)
    elif args.fast_search:
        query = " ".join(args.fast_search)
        fast_search(query, gemini_api_key)
    elif args.listen:
        #  If --listen is used, call the voice processing functions
        command = listen_for_command()
        process_voice_command(command, gemini_api_key)


if __name__ == "__main__":
    main()
