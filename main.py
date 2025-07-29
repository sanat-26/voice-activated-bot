import ctypes
import os
import sys
import speech_recognition as sr
import pyttsx3
import webbrowser
import pyaudio
import musicLibrary
import requests
from openai import OpenAI

# Suppress ALSA warnings
def suppress_alsa_errors():
    ERROR_HANDLER_FUNC = ctypes.CFUNCTYPE(None, ctypes.c_char_p, ctypes.c_int,
                                          ctypes.c_char_p, ctypes.c_int, ctypes.c_char_p)

    def py_error_handler(filename, line, function, err, fmt):
        pass

    c_error_handler = ERROR_HANDLER_FUNC(py_error_handler)
    try:
        asound = ctypes.cdll.LoadLibrary('libasound.so')
        asound.snd_lib_error_set_handler(c_error_handler)
    except:
        pass  # If libasound is missing, just skip

suppress_alsa_errors()

recognizer = sr.Recognizer()
engine = pyttsx3.init()
newsapi = 'd62a5d7f2c3847d0adcb9fd649df7c85'

def speak(text):
    engine.say(text)
    engine.runAndWait()

def process_ai(command):

    client = OpenAI(
    api_key="YOUR_API_KEY"
    )

    completion = client.chat.completions.create(
    model="gpt-4o-mini",
    store=True,
    messages=[
        {"role": "user", "content": command}
    ]
    )

    return completion.choices[0].message


def process_command(c):
    if 'open google' in c.lower():
        webbrowser.open('https://google.com')
    elif 'open youtube' in c.lower():
        webbrowser.open('https://youtube.com')
    elif 'open linkedin' in c.lower():
        webbrowser.open('https://linkedin.com')
    elif c.lower().startswith('play'):
        song = c.lower().split(' ')[1]
        webbrowser.open(musicLibrary.music[song])
    elif 'hello' in c.lower():
        r=requests.get(f'https://newsapi.org/v2/top-headlines?country=us&apiKey={newsapi}')
        if r.status_code == 200:
            data = r.json()
            articles = data.get('articles', [])

            for article in articles[:2]:   #prints only two articles
                speak(article['title'])
                print(f"   URL: {article['url']}\n")
        else:
            print(f"Error: {r.status_code}")
            print(r.text)
    else:
        output = process_ai(c)
        speak(output)

if __name__=='__main__':
    speak('Initialising Java.....')
    while True:
    # obtain audio from the microphone
        r = sr.Recognizer()

        # recognize speech using Sphinx
        print('processing....')
        try:
            with sr.Microphone() as source:
                audio = r.listen(source, timeout=3, phrase_time_limit=3)
                word = r.recognize_google(audio)
                print(f'Heard : {word}')

                if(word.lower()=='hello'):
                    speak('Yeah?')

                    #listen for command
                    with sr.Microphone() as source:
                        print("java active....")
                        audio = r.listen(source, timeout=3, phrase_time_limit=3)
                        command = r.recognize_google(audio)

                        process_command(command)

        except Exception as e:
            print("error; {0}".format(e))