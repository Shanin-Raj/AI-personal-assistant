# Import the necessary libraries
from gtts import gTTS
from playsound import playsound
import os

def speak(text, filename="response.mp3"):
    """
    Converts a string of text into speech and plays it.
    """
    try:
        # 1. Create the gTTS object
        # It takes the text and the language ('en' for English)
        print("-> Converting text to speech...")
        tts = gTTS(text=text, lang='en')

        # 2. Save the converted audio to a file
        tts.save(filename)
        print(f"-> Saved speech to {filename}")

        # 3. Play the audio file
        print("-> Speaking...")
        playsound(filename)

        # 4. Clean up by deleting the audio file
        os.remove(filename)

    except Exception as e:
        print(f"An error occurred in the text-to-speech function: {e}")


# --- Main Program Logic ---
if __name__ == "__main__":
    # A test sentence to speak
    test_sentence = "Hello, this is a test of the text-to-speech functionality. I am now online."
    
    # Call the function to speak the sentence
    speak(test_sentence)

