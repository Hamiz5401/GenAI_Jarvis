# Python program to translate
# speech to text and text to speech
import speech_recognition as sr
import pyttsx3
import os
from dotenv import load_dotenv
import openai
import whisper

tiny_model_path = os.path.expanduser('~/.cache/whisper/tiny.en')
base_model_path = os.path.expanduser('~/.cache/whisper/base.en')
tiny_model = whisper.load_model("tiny")
base_model = whisper.load_model("base")

# Initialize the recognizer
r = sr.Recognizer()

load_dotenv()
OPENAI_KEY = os.getenv('OPENAI_KEY')

openai.api_key = OPENAI_KEY


# Function to convert text to
# speech
def SpeakText(command):
    # Initialize the engine
    engine = pyttsx3.init()
    engine.say(command)
    engine.runAndWait()


# Loop infinitely for user to
# speak

def record_text():
    recognizer = sr.Recognizer()

    with sr.Microphone() as source:
        print("Say something:")
        recognizer.adjust_for_ambient_noise(source, duration=1)
        audio = recognizer.listen(source, timeout=5)

    try:
        text = recognizer.recognize_google(audio)
        print("You said:", text)
        return text
    except sr.UnknownValueError:
        print("Could not understand audio.")
    except sr.RequestError as e:
        print(f"Could not request results from Google Speech Recognition service; {e}")


def send_to_chatgpt(messages, model="gpt-3.5-turbo"):
    response = openai.chat.completions.create(
        model=model,
        messages=messages,
        max_tokens=100,
        n=1,
        stop=None,
        temperature=0.5
    )

    message = response.choices[0].message.content
    messages.append(response.choices[0].message)
    return message


messages = []
while (1):
    text = record_text()
    messages.append({"role": "user", "content": text})
    response = send_to_chatgpt(messages)
    SpeakText(response)

    print(response)
