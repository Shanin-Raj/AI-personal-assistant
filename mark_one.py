# Import all necessary libraries
import argparse
import requests 
import os                          # For file operations
from dotenv import load_dotenv     # For loading environment variables
import wikipediaapi                # For Wikipedia searches
import speech_recognition as sr    # For voice recognition
import json                        # For JSON handling
from datetime import datetime      # For timestamping notes
from gtts import gTTS              # For text-to-speech
from playsound import playsound    # For playing audio files

# Load environment variables from the .env file
load_dotenv()

# --- Text-to-Speech Function ---
def speak(text, tld='co.uk', filename="response.mp3"): 
    """Converts a string of text into speech and plays it."""
    try:
        # Clean the text by removing any special characters that might cause issues
        clean_text = text.replace('*', '').replace('#', '')

        print("-> Converting text to speech...")
        # Pass the tld to gTTS to change the accent
        tts = gTTS(text=clean_text, lang='en', tld=tld)
        tts.save(filename)
        print("-> Speaking...")
        playsound(filename)
        os.remove(filename) # Clean up the audio file
    except Exception as e:
        print(f"An error occurred in the text-to-speech function: {e}")

# --- Feature Functions ---

def fast_search(query, api_key):
    """Uses the Gemini AI to directly answer a user's query."""
    print(f"-> Asking Gemini for a quick summary of: '{query}'...")
    prompt = (f"Please provide a concise summary that directly answers the following query.It should be presented in a neat way.\nQuery: '{query}'")
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash-latest:generateContent?key={api_key}"
    payload = {"contents": [{"parts": [{"text": prompt}]}]}
    headers = {'Content-Type': 'application/json'}
    try:
        response = requests.post(url, json=payload, headers=headers, timeout=20)
        response.raise_for_status()
        data = response.json()
        summary = data['candidates'][0]['content']['parts'][0]['text'].strip()
        print(f"\n--- AI Generated Summary ---\n{summary}")
        speak(summary) # Speak the result
    except Exception as e:
        error_message = f"An error occurred: {e}"
        print(error_message)
        speak(error_message)

def structured_search(query, api_key):
    """Uses AI to optimize a search term and then searches Wikipedia."""
    print(f"-> Optimizing search term with AI...")
    prompt = (f"Based on the following user query, what is the best possible search term for Wikipedia? Respond with only the ideal search term and nothing else.\nQuery: '{query}'")
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
        not_found_message = f"Sorry, I could not find a Wikipedia page for '{optimized_term}'."
        print(not_found_message)
        speak(not_found_message)
        return

    result_title = f"Here is a summary for {page.title}."
    summary_sentences = page.summary.split('.')
    result_summary = ". ".join(summary_sentences[:3]) + "."
    print(f"\n--- Result for: {page.title} ---\n{result_summary}")
    speak(result_title + " " + result_summary) # Speak the result

def get_news_summary(gemini_api_key, news_api_key, country='in'):
    """Fetches top headlines from GNews and uses Gemini to summarize them."""
    print(f"-> Fetching top headlines for country: '{country}'...")
    try:
        url = f"https://gnews.io/api/v4/top-headlines?apikey={news_api_key}&lang=en&country={country}&max=5"
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()
        articles = data.get('articles', [])
        if not articles:
            no_headlines_message = "Sorry, I could not find any top headlines."
            print(no_headlines_message)
            speak(no_headlines_message)
            return
        headlines = [article['title'] for article in articles]
    except requests.exceptions.RequestException as e:
        error_message = f"Error fetching news data: {e}"
        print(error_message)
        speak(error_message)
        return

    print("-> Summarizing headlines with AI...")
    headlines_text = "\n".join(headlines)
    prompt = (f"You are a news anchor. Based on the following headlines, provide a concise and neat summary of today's top news in  bulleted list, with each point summarizing one key event.\n\nHeadlines:\n{headlines_text}")
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash-latest:generateContent?key={gemini_api_key}"
    payload = {"contents": [{"parts": [{"text": prompt}]}]}
    headers = {'Content-Type': 'application/json'}
    try:
        response = requests.post(url, json=payload, headers=headers, timeout=20)
        response.raise_for_status()
        data = response.json()
        summary = data['candidates'][0]['content']['parts'][0]['text'].strip()
        print(f"\n--- Today's News Summary ---\n{summary}")
        speak("Here is a summary of today's top news. " + summary) # Speak the result
    except Exception as e:
        error_message = f"An error occurred during summarization: {e}"
        print(error_message)
        speak(error_message)

def add_note(note_text):
    """Appends a new note with a timestamp to the notes.txt file."""
    with open("notes.txt", "a") as file:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        file.write(f"[{timestamp}] {note_text}\n")
    success_message = "Note saved successfully."
    print(f"-> {success_message}")
    speak(success_message) # Speak the confirmation

def view_notes():
    """Reads and prints all notes from the notes.txt file."""
    try:
        with open("notes.txt", "r") as file:
            notes = file.read()
            if notes:
                print("\n--- Your Notes ---")
                print(notes)
                speak("Here are your notes.")
                # We don't speak the full notes as it could be long.
            else:
                no_notes_message = "You don't have any notes yet."
                print(no_notes_message)
                speak(no_notes_message)
    except FileNotFoundError:
        no_file_message = "You don't have any notes yet. Add one first!"
        print(no_file_message)
        speak(no_file_message)

# --- Voice and Intent Recognition Functions ---

def listen_for_command(prompt="Awaiting your command..."):
    """Listens for a command from the microphone and returns the recognized text."""
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print(prompt)
        r.adjust_for_ambient_noise(source, duration=0.5)
        try:
            audio = r.listen(source, timeout=5, phrase_time_limit=10)
            print("Recognizing...")
            text = r.recognize_google(audio)
            print(f"-> You said: '{text}'")
            return text.lower()
        except Exception as e:
            print(f"An error occurred during listening: {e}")
            return None

def get_command_intent(user_command, api_key):
    """The 'Brain' of the assistant. Uses Gemini to determine the user's intent."""
    print(f"-> Analyzing command intent with AI...")
    prompt = (
        "You are the brain of a personal AI assistant. Your job is to analyze the user's command "
        "and determine their intent. The possible intents are 'get_news', 'search', 'fast_search', 'add_note', 'view_notes', and 'unknown'.\n\n"
        "Analyze the following command and respond with ONLY a JSON object containing two keys: "
        "'intent' and 'query'.\n"
        "- 'intent' must be one of the possible intents.\n"
        "- 'query' is the main subject of the user's command. For news or viewing notes, the query should be 'general'.\n\n"
        f"Command: '{user_command}'"
    )

    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash-latest:generateContent?key={api_key}"
    payload = {"contents": [{"parts": [{"text": prompt}]}]}
    headers = {'Content-Type': 'application/json'}

    try:
        response = requests.post(url, json=payload, headers=headers, timeout=20)
        response.raise_for_status()
        data = response.json()
        response_text = data['candidates'][0]['content']['parts'][0]['text']
        start_index = response_text.find('{')
        end_index = response_text.rfind('}') + 1
        json_string = response_text[start_index:end_index]
        intent_data = json.loads(json_string)
        return intent_data
    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 503:
            print("Error: The AI service is temporarily unavailable. Please try again in a moment.")
        else:
            print(f"An HTTP error occurred: {e}")
        return {"intent": "unknown", "query": "error"}
    except Exception as e:
        print(f"Error processing intent: {e}")
        return {"intent": "unknown", "query": "error"}

# --- Main Controller ---
def main():
    parser = argparse.ArgumentParser(description="Mark I: Your Personal AI Assistant. Run without arguments to listen for a voice command.")
    args = parser.parse_args()
    
    gemini_api_key = os.getenv("GEMINI_API_KEY")
    news_api_key = os.getenv("NEWS_API_KEY")

    if not gemini_api_key or not news_api_key:
        print("Error: API keys not found in .env file.")
        return

    # Greet the user with voice
    speak("Mark I online sir. How can I help you ?")

    command_text = listen_for_command()
    
    if command_text:
        intent_data = get_command_intent(command_text, gemini_api_key)
        intent = intent_data.get('intent')
        query = intent_data.get('query')

        if intent == 'get_news':
            get_news_summary(gemini_api_key, news_api_key)
        elif intent == 'search':
            structured_search(query, gemini_api_key)
        elif intent == 'fast_search':
            fast_search(query, gemini_api_key)
        elif intent == 'add_note':
            speak("What should the note say?")
            note_content = listen_for_command(prompt="Listening for your note...")
            if note_content:
                add_note(note_content)
        elif intent == 'view_notes':
            view_notes()
        else:
            unrecognized_message = "Sorry, I couldn't determine your intent. Please try again."
            print(unrecognized_message)
            speak(unrecognized_message)

if __name__ == "__main__":
    main()
