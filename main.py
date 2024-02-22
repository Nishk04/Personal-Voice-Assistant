import speech_recognition as sr
import pyttsx3
import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI(api_key=os.environ.get("api_key"),)

# Converts text to speech
def SpeakToText(answer):
    # Initializes engine
    engine = pyttsx3.init()
    # Tells the engine to say the text
    engine.say(answer)
    engine.runAndWait()

# Initializes the voice recognizer
r = sr.Recognizer()

def record_text():
    # To check for errors when speaking
    try:
        # Our source of input
        with sr.Microphone() as source:
            # Prepare recognizer to receive input
            r.adjust_for_ambient_noise(source, duration=0.2)
            
            print("I'm listening")

            # Listens for user's input
            audio = r.listen(source)
            
            # Uses google to recognize audio
            MyText = r.recognize_google(audio)

            return MyText

    except sr.RequestError as e:
        print("Could not request results; {0}".format(e))
        
    except sr.UnknownValueError:
        print("Unknown error occurred.")

def SendToChatGPT(messages, model="gpt-3.5-turbo"):
    response = client.chat.completions.create(
        model=model,
        messages=messages,
        max_tokens=100, # Lets ChatGPT know how many characters it can use in its response
        n=1,
        stop=None,
        temperature=0.5
    )

    message = response.choices[0].message.content  # Access content from first message it sends
    messages.append({"role": "user", "content": message})
    return message

messages = []

while True:
    text = record_text()
    if text == "stop listening" or text == "end program Jarvis":
        print("Ended program")
        break
    print(text)
    messages.append({"role": "user", "content": text})
    response = SendToChatGPT(messages)
    SpeakToText(response)
    print(response)
