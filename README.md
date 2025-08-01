# Project Mark I: AI Personal Assistant

This repository contains the code for **"Mark I"**, a personal command-line assistant built with Python. This project is a semester-long endeavor to build an intelligent assistant from the ground up, learning and integrating new technologies with each new version ("Mark").

---

## Current Features

### Dual Search Modes
- **--search**: Structured search mode that uses AI to optimize a user's query and retrieves a factual summary from Wikipedia.
- **--fast-search**: Quick search mode that uses the Gemini AI to provide a direct, concise summary for any question.

### Voice Command Interface
- **--listen**: Activates the microphone to allow the user to speak their commands (e.g., "search what is an array in C").

---

## Technologies Used

- **Language**: Python 3

### Core Libraries
- `argparse`: For parsing command-line arguments.
- `requests`: For making API calls.
- `python-dotenv`: For secure management of API keys.

### Voice & AI
- `SpeechRecognition`: To capture and convert microphone audio to text.
- `PyAudio`: As a dependency for microphone access.

### APIs
- Google Gemini API
- Wikipedia-API

---

## How to Run This Project

1. **Clone the repository:**
    ```sh
    git clone https://github.com/Shanin-Raj/AI-personal-assistant.git
    cd AI-personal-assistant
    ```

2. **Install the required libraries:**
    ```sh
    pip install requests python-dotenv wikipedia-api SpeechRecognition PyAudio
    ```

3. **Create your `.env` file:**
    - Create a file named `.env` in the main project folder and add your Gemini API key:
      ```
      GEMINI_API_KEY=YOUR_GEMINI_KEY_HERE
      ```

4. **Run a command:**
    - **Text Search:**
      ```sh
      python mark_one.py --search "your query here"
      ```
    - **Fast AI Search:**
      ```sh
      python mark_one.py --fast-search "your query here"
      ```
    - **Voice Command:**
      ```sh
      python mark_one.py --listen
      ```
      Then, say your command (e.g., "search for the history of Python").

---

## Project Development History

This project is being built in phases, with each "Mark" representing a new set of capabilities.

- **Mark I: The Foundation (Completed)**
    - Initial project setup and repository creation.
    - Implementation of a robust command-line argument parser.

- **Mark II: The Search Module (Completed)**
    - Added dual search modes (`--search` and `--fast-search`).
    - Integrated Google Gemini and Wikipedia APIs.
    - Implemented voice command interface using the `--listen` command.

- **Mark III: The Information Hub (Upcoming)**
    - News Summaries: Add a command to fetch and summarize top news headlines.
    - Note-Taking: Implement commands to add and view personal notes.

- **Mark IV: The Vision System (Upcoming)**
    - Webcam Access: Integrate OpenCV to access the system's webcam.
    - Basic Monitoring: Implement a simple security feature to detect faces in the camera feed.