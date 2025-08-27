import speech_recognition 
import pyttsx3

engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)
engine.setProperty('rate', 150)

def speak(audio):
    engine.say(audio)
    engine.runAndWait()

def takeCommand():
    """Listen for a voice command and return the recognized text."""
    r = speech_recognition.Recognizer()
    with speech_recognition.Microphone() as source:
        print("I'm listening... Please speak clearly.")
        r.pause_threshold = 1.0
        r.energy_threshold = 189
        try:
            audio = r.listen(source, timeout=10)
        except Exception as e:
            print("Sorry, I couldn't hear anything. Please check your microphone.")
            return "None"
    try:
        print("Processing your command...")
        query = r.recognize_google(audio, language='en-in')
        print(f"You said: {query}\n")
        return query
    except Exception as e:
        return "None"

query = takeCommand().lower()
