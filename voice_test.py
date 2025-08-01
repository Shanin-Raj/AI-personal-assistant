# Import the speech_recognition library
import speech_recognition as sr

def recognize_speech_from_mic():
    """
    Listens for a single command from the microphone and converts it to text.
    """
    # 1. Create a Recognizer instance
    r = sr.Recognizer()

    # 2. Use the microphone as the audio source
    with sr.Microphone() as source:
        print("Calibrating microphone for a moment...")
        # Adjust for ambient noise to improve accuracy
        r.adjust_for_ambient_noise(source, duration=1)
        
        print("Listening... Say something!")
        
        # Listen for the first phrase and extract it into audio data
        try:
            audio = r.listen(source, timeout=5, phrase_time_limit=5)
        except sr.WaitTimeoutError:
            print("Timeout: No speech was detected.")
            return None

    # 3. Recognize speech using Google's free web API
    print("Recognizing...")
    try:
        # The recognize_google() function sends the audio data to Google's API
        text = r.recognize_google(audio)
        return text
    except sr.UnknownValueError:
        # This error happens when the API can't understand the audio
        print("Google Web Speech API could not understand the audio.")
        return None
    except sr.RequestError as e:
        # This error happens if there's a problem with the API request
        print(f"Could not request results from Google Web Speech API; {e}")
        return None

# --- Main Program Logic ---
if __name__ == "__main__":
    # Call the function to listen and recognize
    recognized_text = recognize_speech_from_mic()

    # Print the result if successful
    if recognized_text:
        print(f"\nI heard you say: '{recognized_text}'")

