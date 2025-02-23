import os
import psutil
import subprocess
import requests
import tkinter as tk
from tkinter import scrolledtext
import threading
import pyttsx3
import speech_recognition as sr
import datetime
import randfacts
from selenium_web import *
from YT_audio import *
from News import *
from jokes import *
from ss import *

ASSISTANT_NAME = "Sifra"

# Initialize speech engine
engine = pyttsx3.init()
engine.setProperty('rate', 140)
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)

# Initialize speech recognizer
r = sr.Recognizer()


# Function to speak
def speak(text):
    """Function to convert text to speech and update UI"""
    chat_window.insert(tk.END, "Assistant: " + text + "\n")
    chat_window.yview(tk.END)
    engine.say(text)
    engine.runAndWait()


# Function to greet
def wishme():
    hour = int(datetime.datetime.now().hour)
    if 0 <= hour < 12:
        return "Good morning"
    elif 12 <= hour < 18:
        return "Good afternoon"
    else:
        return "Good evening"


# Function to get current time
def tell_time():
    """Function to get and speak the current time"""
    now = datetime.datetime.now().strftime("%I:%M %p")  # Format: 12-hour format with AM/PM
    speak(f"The time is {now}")


# Function to get weather
def get_weather(city="your_city"):
    """Function to fetch and speak weather details"""
    API_KEY = key2  # Replace with your OpenWeather API key
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"

    try:
        response = requests.get(url)
        data = response.json()

        if data["cod"] != 200:
            speak("Sorry, I couldn't fetch the weather details.")
            return

        temp = data["main"]["temp"]
        weather_description = data["weather"][0]["description"]
        speak(f"The current temperature in {city} is {temp} degrees Celsius with {weather_description}.")
    except Exception as e:
        speak("There was an issue fetching the weather. Please try again.")


# Function to open applications
def open_application(app_name):
    try:
        if "notepad" in app_name:
            os.system("notepad.exe")
        elif "chrome" in app_name:
            os.system("start chrome")
        elif "calculator" in app_name:
            os.system("calc.exe")
        elif "whatsapp" in app_name:
            os.system("start whatsapp.exe")  # Works if WhatsApp Desktop is installed
        else:
            speak("Sorry, I cannot open this application.")
    except Exception as e:
        speak(f"Error opening application: {e}")


# Function to close applications
def close_application(app_name):
    try:
        found = False
        for process in psutil.process_iter(['pid', 'name']):
            if app_name.lower() in process.info['name'].lower():
                # speak(f"Closing {process.info['name']}...")
                psutil.Process(process.info['pid']).terminate()
                found = True
                break
        if not found:
            speak(f"Application '{app_name}' is not running.")
    except Exception as e:
        speak(f"Error closing application: {e}")


# Function to process commands
def process_command():
    while True:
        try:
            with sr.Microphone() as source:
                r.energy_threshold = 10000
                r.adjust_for_ambient_noise(source, 1.2)
                chat_window.insert(tk.END, "Listening...\n")
                chat_window.yview(tk.END)

                audio = r.listen(source)
                text = r.recognize_google(audio).lower()

                chat_window.insert(tk.END, "You: " + text + "\n")
                chat_window.yview(tk.END)

            if "exit" in text or "stop" in text or "goodbye" in text or "good bye" in text:
                speak("Goodbye sir! Have a great day.")
                root.quit()

            elif "i am fine" in text or "i'm fine" in text:
                speak("I am glad to hear that, sir. How can I assist you?")

            elif "what time is it" in text or "time" in text or "tell me the time" in text:
                tell_time()


            elif "weather" in text or "tell me the weather" in text:
                speak("Please tell me the name of your city.")

                with sr.Microphone() as source:
                    r.adjust_for_ambient_noise(source, 1.2)
                    audio = r.listen(source)
                    city = r.recognize_google(audio)

                speak(f"Fetching weather for {city}...")
                weather_info = get_weather(city)  # Get weather data
                speak(weather_info)

            elif "what is your name" in text or "who are you" in text or "your name" in text:
                speak(f"My name is {ASSISTANT_NAME}. I am your voice assistant.")

            elif "information" in text:
                speak("You need information related to which topic?")
                with sr.Microphone() as source:
                    r.adjust_for_ambient_noise(source, 1.2)
                    audio = r.listen(source)
                    infor = r.recognize_google(audio)

                speak(f"Searching {infor} on Wikipedia")
                assist = Info()
                assist.get_info(infor)

            elif "play" in text and "video" in text or "song" in text:
                speak("You want to play which video?")
                with sr.Microphone() as source:
                    r.adjust_for_ambient_noise(source, 1.2)
                    audio = r.listen(source)
                    vid = r.recognize_google(audio)

                speak(f"Playing {vid} video on YouTube")
                assist = Music()
                assist.play(vid)

            elif "news" in text:
                speak("Sure sir, now I will read news for you.")
                arr = news()
                for item in arr:
                    speak(item)

            elif "fact" in text or "facts" in text:
                speak("Sure sir, now I will read a fact for you.")
                fact = randfacts.get_fact()
                speak(f"Did you know that, {fact}")

            elif "joke" in text or "jokes" in text:
                speak("Sure sir, get ready for some chuckles.")
                arr = joke()
                speak(arr[0])
                speak(arr[1])

            elif "open" in text:
                app_name = text.replace("open", "").strip()
                speak(f"Opening {app_name}...")
                open_application(app_name)

            elif "close" in text:
                app_name = text.replace("close", "").strip()
                speak(f"Closing {app_name}...")
                close_application(app_name)

            else:
                speak("I didn't understand that. Can you please repeat?")

        except sr.UnknownValueError:
            speak("Sorry, I couldn't understand. Can you say that again?")
            continue
        except sr.RequestError:
            speak("There is a problem with the speech recognition service. Please check your internet connection.")
            continue
        except Exception as e:
            chat_window.insert(tk.END, f"Error: {e}\n")
            chat_window.yview(tk.END)
            speak("An error occurred. Please try again.")
            continue


# Function to start voice assistant in a separate thread
def start_assistant():
    threading.Thread(target=process_command, daemon=True).start()


# Creating the UI using Tkinter
root = tk.Tk()
root.title("Voice Assistant")
root.geometry("500x600")
root.resizable(False, False)

# Function to exit
def exit_app():
    speak("Goodbye sir! Have a great day.")
    root.quit()


# Create a frame for chat window
chat_frame = tk.Frame(root)
chat_frame.pack(pady=10)

# Scrollable text box
chat_window = scrolledtext.ScrolledText(chat_frame, wrap=tk.WORD, width=60, height=20)
chat_window.pack()

# Buttons
start_button = tk.Button(root, text="Start Listening", command=start_assistant, bg="green", fg="white",
                         font=("Arial", 12))
start_button.pack(pady=10)

exit_button = tk.Button(root, text="Exit", command=exit_app, bg="red", fg="white", font=("Arial", 12))
exit_button.pack()

# Greeting message
speak(f"Hello sir, {wishme()} I am {ASSISTANT_NAME}, your voice assistant.")
speak("Click the Start Listening button to give a command.")

# Run the UI
root.mainloop()
