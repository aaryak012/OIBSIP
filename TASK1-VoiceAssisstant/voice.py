"""
Voice Assistant - Beginner Tier
--------------------------------
Features:
  1. Capture voice input via microphone (speech_recognition)
  2. Respond to "hello" with a greeting
  3. Tell current time and date
  4. Perform a web search on a spoken topic
  5. Graceful error handling (asks user to repeat if unclear)
  6. Text-to-speech feedback for every response (pyttsx3)

Install dependencies before running:
    pip install SpeechRecognition pyttsx3 pyaudio

Windows note: if `pip install pyaudio` fails, run:
    pip install pipwin
    pipwin install pyaudio

Mac note: you may need `brew install portaudio` before pip install pyaudio
Linux note: you may need `sudo apt-get install portaudio19-dev python3-pyaudio`
"""

import speech_recognition as sr
import pyttsx3
import datetime
import webbrowser


# ---------- Text-to-Speech Setup ----------
engine = pyttsx3.init()
engine.setProperty("rate", 175)   # speaking speed
engine.setProperty("volume", 1.0)  # 0.0 to 1.0


def speak(text):
    """Speak the given text out loud and print it to the console."""
    print(f"Assistant: {text}")
    engine.say(text)
    engine.runAndWait()


# ---------- Speech Recognition Setup ----------
recognizer = sr.Recognizer()


def listen():
    """
    Listen to the microphone and return recognized text (lowercase),
    or None if speech wasn't understood / an error occurred.
    """
    with sr.Microphone() as source:
        print("\nListening... (speak now)")
        recognizer.adjust_for_ambient_noise(source, duration=0.5)
        try:
            audio = recognizer.listen(source, timeout=5, phrase_time_limit=8)
        except sr.WaitTimeoutError:
            speak("I didn't hear anything. Please try again.")
            return None

    try:
        command = recognizer.recognize_google(audio)
        print(f"You said: {command}")
        return command.lower()
    except sr.UnknownValueError:
        # Speech was unintelligible
        speak("Sorry, I didn't catch that. Could you please repeat?")
        return None
    except sr.RequestError:
        speak("Speech service is unavailable right now. Check your internet connection.")
        return None


# ---------- Command Handlers ----------
def handle_greeting():
    speak("Hello there! How can I help you today?")


def handle_time_and_date():
    now = datetime.datetime.now()
    current_time = now.strftime("%I:%M %p")
    current_date = now.strftime("%A, %B %d, %Y")
    speak(f"It is currently {current_time} on {current_date}.")


def handle_web_search(command):
    # Remove trigger words to isolate the search topic
    trigger_words = ["search for", "search", "look up", "google"]
    topic = command
    for word in trigger_words:
        topic = topic.replace(word, "")
    topic = topic.strip()

    if topic:
        speak(f"Searching the web for {topic}")
        url = f"https://www.google.com/search?q={topic.replace(' ', '+')}"
        webbrowser.open(url)
    else:
        speak("What would you like me to search for?")
        follow_up = listen()
        if follow_up:
            speak(f"Searching the web for {follow_up}")
            url = f"https://www.google.com/search?q={follow_up.replace(' ', '+')}"
            webbrowser.open(url)


def handle_exit():
    speak("Goodbye! Have a great day.")


# ---------- Main Loop ----------
def run_assistant():
    speak("Voice assistant is ready. Say 'hello', ask for the 'time', 'date', "
          "say 'search for <topic>', or say 'exit' to quit.")

    while True:
        command = listen()

        if command is None:
            # Error already handled inside listen(); just loop again
            continue

        if "hello" in command or "hi " in command or command.strip() == "hi":
            handle_greeting()

        elif "time" in command or "date" in command:
            handle_time_and_date()

        elif "search" in command or "look up" in command or "google" in command:
            handle_web_search(command)

        elif "exit" in command or "quit" in command or "stop" in command:
            handle_exit()
            break

        else:
            speak("I'm not sure how to help with that yet. "
                  "Try saying hello, asking for the time, or searching for a topic.")


if __name__ == "__main__":
    try:
        run_assistant()
    except KeyboardInterrupt:
        speak("Shutting down. Goodbye!")