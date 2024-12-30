from random import sample
import speech_recognition as sr
import datetime
import os
import google.generativeai as genai
import subprocess
from PIL import Image
import pypdf
import pathlib


genai.configure(api_key="AIzaSyAio8rDBVYAhP-gfkFjgV-6vc7YWy0dDZE")
model = genai.GenerativeModel("gemini-1.5-flash")



# text to speech
def speak(audio, speed=200):
    # Escape double quotes in the audio string for AppleScript compatibility
    escaped_audio = audio.replace('"', '\\"')
    # Construct the AppleScript command
    script = f'say "{escaped_audio}" using "Karen" speaking rate {speed}'
    # Run the script using subprocess
    subprocess.run(['osascript', '-e', script])

def takecommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("listening...")
        r.pause_threshold = 2
        audio = r.listen(source, timeout=2, phrase_time_limit=60)

    i = 0
    query='say nothing'
    while (i < 1):
        try:
            print("Recognizing...")
            # query = r.recognize_google(audio, language='en-in')
            query = r.recognize_google(audio, language='en-in')
            print(f"user said: {query}")

        except:
            print('Say that again please.')
        i = i + 1
    return query


def wish():
    speak("Hello!",speed=200)

def extract_text_from_pdf(pdf_path):
    with open(pdf_path, 'rb') as pdf_file:
        pdf_reader = pypdf.PdfReader(pdf_file)
        extracted_text = ""
        for page in pdf_reader.pages:
            text = page.extract_text()
            if text:
                extracted_text += text
        return extracted_text

if __name__ == "__main__":
    wish()
    if 1:
        query = takecommand().lower()
        question = query
        response = model.generate_content("Print IDK What")
        if "open" in question:
            response = model.generate_content(
                "Write a python code to" + question + "on mac. You can use any module which will not require a path to open.")
            text1 = response.text
            text = text1.split("```python")
            text = text[1]
            text = text.split("```")[0]
            f = open("file.py", "w")
            f.write(text)
            f.close()
            subprocess.run(["python", "file.py"])
        elif "search" in question:
            response = model.generate_content("Write a python code to open chrome and search " + question + " on google chrome on mac. If you want directly insert the link.")
            text1 = response.text
            text = text1.split("```python")
            text = text[1]
            text = text.split("```")[0]
            f = open("file.py", "w")
            f.write(text)
            f.close()
            subprocess.run(["python", "file.py"])
        elif "analyze" in question and 'screen' in question:
            response = model.generate_content("Write a python code to take a screenshot of the screen and save it as screenshot1 in the SFP folder of Desktop. use pyscreenshot")
            text1 = response.text
            text = text1.split("```python")
            text = text[1]
            text = text.split("```")[0]
            f = open("file.py", "w")
            f.write(text)
            f.close()
            subprocess.run(["python", "file.py"])
            img = Image.open('/Users/macbookpro/Desktop/SFP/screenshot1.png')
            response1 = model.generate_content(["Tell me about this in one paragraph", img])
            r1 = str(response1.text)
            try:
                r1=r1.split["\n"]
                r1=r1[0]
            except:
                print("")
            print(r1)
            speak(r1)
        elif "analyze" in question and 'image' in question:
            response = model.generate_content("Using the question, give me the folder and the filename in minimum words required"+question+"give it in the form folder/filename")
            text1 = response.text.split('\n')[0]
            img = Image.open('/Users/macbookpro/'+text1)
            response1 = model.generate_content(["Tell me about this in one paragraph", img])
            r1 = str(response1.text)
            try:
                r1=r1.split["\n"]
                r1=r1[0]
            except:
                print("")
            speak(r1)
        elif "analyze" in question and ('pdf' in question or 'PDF' in question):
            response = model.generate_content("Using the question, give me the folder and the filename in minimum words required"+question+"give it in the form folder/filename")
            text1 = str(response.text.split('\n')[0])
            sample_pdf = extract_text_from_pdf('/Users/macbookpro/'+text1)
            response1 = model.generate_content(["Tell me about this in one paragraph", sample_pdf])
            r1 = str(response1.text)
            try:
                r1=r1.split["\n"]
                r1=r1[0]
            except:
                print("")
            speak(r1)
        elif "translate" in question:
            response = model.generate_content("Write a python code to take a screenshot of the screen and save it as screenshot1 in the SFP folder of Desktop. use pyscreenshot")
            text1 = response.text
            text = text1.split("```python")
            text = text[1]
            text = text.split("```")[0]
            f = open("file.py", "w")
            f.write(text)
            f.close()
            subprocess.run(["python", "file.py"])
            img = Image.open('/Users/macbookpro/Desktop/SFP/screenshot1.png')
            response1 = model.generate_content(["Translate the image in 1 paragraph", img])
            r1 = str(response1.text)
            try:
                r1=r1.split["\n"]
            except:
                print("")
            lst=["one"]
            lst.append(r1)
            if len(lst)>2:
                for k in r1:
                    speak(k)
                    print(k)
            else:
                speak(r1)
        elif "take" in question:
            response = model.generate_content("Write a python code to " + question + " . Use pyscreenshot.")
            text1 = response.text
            text = text1.split("```python")
            text = text[1]
            text = text.split("```")[0]
            f = open("file.py", "w")
            f.write(text)
            f.close()
            subprocess.run(["python", "file.py"])
        else:
            response = model.generate_content("Answer the question: " + question + "give the answer in plain text")
            speak(response.text)
            f = open("file.py", "w")
            f.write(" ")
            f.close()
