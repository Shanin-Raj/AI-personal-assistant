# Project S.H.A.N.I.N. - Mark I Release

This repository contains the code for the Mark I version of my personal AI assistant, S.H.A.N.I.N.  
A semester-long project to build an intelligent assistant from the ground up, integrating new technologies with each version.

---

## Core Features

- **Voice-Controlled Interface**  
  Interact with the assistant using voice commands. It listens, understands your intent, and responds with synthesized speech.

- **Intelligent Search**
  - **Fact-Checked Answers:** Optimizes your question for Wikipedia and provides a structured, factual summary.
  - **Quick Summaries:** Uses Gemini AI to provide fast, direct answers for any query.
  - **News Briefing:** Fetches the latest news headlines for a country and delivers a concise, AI-powered summary.

- **Personal Note-Taking**
  - **Add Notes:** Save personal notes with a timestamp using a simple voice command.
  - **View Notes:** Display all your saved notes in the terminal.

---

## Technologies Used

- **Language:** Python 3

- **AI & APIs:**
  - Intent Recognition: Google Gemini API
  - Information Retrieval: Wikipedia-API, GNews API
  - Voice Recognition: SpeechRecognition library
  - Text-to-Speech: gTTS (Google Text-to-Speech) library

- **Core Libraries:**
  - `requests`: For API communication
  - `python-dotenv`: For secure management of API keys
  - `playsound`: To play audio responses

---

## How to Run This Project

1. **Clone the repository:**
    ```sh
    git clone https://github.com/Shanin-Raj/AI-personal-assistant.git
    cd AI-personal-assistant
    ```

2. **Install the required libraries:**
    ```sh
    pip install requests python-dotenv wikipedia-api SpeechRecognition PyAudio gTTS playsound==1.2.2
    ```

3. **Create your `.env` file:**  
   In the main project folder, add your API keys:
    ```
    GEMINI_API_KEY=YOUR_GEMINI_KEY_HERE
    NEWS_API_KEY=YOUR_GNEWS_KEY_HERE
    ```

4. **Run the assistant:**  
   The assistant starts in voice mode automatically.
    ```sh
    python mark_one.py
    ```

5. **Example Commands:**  
   After the prompt, you can say:
   - "What are today's top news headlines?"
   - "Search for the history of the C programming language."
   - "Add a note."

---

## Project Roadmap

This project is built in phases, with each "Mark" representing new capabilities.

- **Mark I: The Information Assistant (Completed ✅)**
  - Initial project setup and command-line structure
  - Integrated APIs for search (Gemini, Wikipedia) and news (GNews)
  - Full voice-controlled interface (Speech-to-Text and Text-to-Speech)
  - Personal productivity features like note-taking

- **The Vision System (Upcoming)**
  - Webcam Access: Integrate OpenCV to access the system's webcam
  - Basic Monitoring: Implement a simple security feature to detect faces in the camera feed