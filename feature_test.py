# Import all necessary libraries
import argparse
import requests 
import os
from dotenv import load_dotenv
import wikipediaapi # We need this library again
import sys # To check for command-line arguments

# Load environment variables
load_dotenv()

# --- Function for Mode 1: Fast AI Summary ---
def get_ai_summary(query, api_key):
    """
    Uses the Gemini AI to directly answer a user's query.
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


# --- Functions for Mode 2: Structured Wikipedia Search ---
def get_optimized_search_term(query, api_key):
    """
    Uses the Gemini AI to convert a natural language query
    into an optimal Wikipedia search term.
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
        return optimized_term
    except Exception as e:
        print(f"An error occurred during optimization: {e}")
        return query

def get_structured_wiki_answer(query):
    """
    Searches Wikipedia for a given query and prints a structured summary.
    """
    print(f"-> Searching Wikipedia for '{query}'...")
    wiki_wiki = wikipediaapi.Wikipedia(user_agent='Mark-I-Assistant/1.0', language='en')
    page = wiki_wiki.page(query)

    if not page.exists():
        print(f"Sorry, I could not find a Wikipedia page for '{query}'.")
        return

    print(f"\n--- Result for: {page.title} ---")
    summary_sentences = page.summary.split('.')
    print(". ".join(summary_sentences[:3]) + ".")


# --- Main Program Logic ---
if __name__ == "__main__":
    gemini_api_key = os.getenv("GEMINI_API_KEY")
    if not gemini_api_key:
        print("Error: GEMINI_API_KEY not found in .env file.")
    
    # NEW: Check if command-line arguments were provided
    # len(sys.argv) will be 1 if only the script name is present.
    if len(sys.argv) > 1:
        # --- MODE 1: Fast AI Summary (Arguments Provided) ---
        parser = argparse.ArgumentParser(description="Get a fast AI-generated summary.")
        parser.add_argument("query", type=str, nargs='+', help="The question you want to ask.")
        args = parser.parse_args()
        user_query = " ".join(args.query)
        get_ai_summary(user_query, gemini_api_key)
    else:
        # --- MODE 2: Structured Search (No Arguments) ---
        # REMOVED the while loop for a single execution.
        print("--- Interactive Structured Search Mode ---")
        user_query = input("Ask a question to get a fact-checked summary from Wikipedia: ")
        if user_query:
            optimized_term = get_optimized_search_term(user_query, gemini_api_key)
            get_structured_wiki_answer(optimized_term)

