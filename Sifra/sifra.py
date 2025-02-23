import os
import psutil
import requests
import tkinter as tk
from tkinter import scrolledtext
import threading
import pyttsx3
import speech_recognition as sr
import datetime
import randfacts
import openai
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

# Assistant Name
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
    chat_window.insert(tk.END, "Assistant: " + text + "\n")
    chat_window.yview(tk.END)
    engine.say(text)
    engine.runAndWait()

# Function to introduce itself
def introduce():
    speak(f"Hello, I am {ASSISTANT_NAME}, your personal voice assistant. I can help you with tasks such as fetching the weather, telling the time, providing news updates, and much more. How can I assist you today?")

# OpenAI API Key (Replace with your API key)
OPENAI_API_KEY = "#####################################################"
openai.api_key = OPENAI_API_KEY

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
    now = datetime.datetime.now().strftime("%I:%M %p")
    speak(f"The time is {now}")

# Function to fetch weather
def get_weather(city="your_city"):
    weather_API_KEY = "################################"  # Replace with your OpenWeather API key
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={weather_API_KEY}&units=metric"
    try:
        response = requests.get(url)
        data = response.json()
        if data["cod"] != 200:
            speak("Sorry, I couldn't fetch the weather details.")
            return
        temp = data["main"]["temp"]
        weather_description = data["weather"][0]["description"]
        speak(f"The current temperature in {city} is {temp} degrees Celsius with {weather_description}.")
    except:
        speak("There was an issue fetching the weather. Please try again.")

# Function to fetch news
def get_news():
    news_api_key = "##################################"
    api_address = f"https://newsapi.org/v2/top-headlines?country=in&apiKey={news_api_key}"

    try:
        json_data = requests.get(api_address).json()

        if "articles" not in json_data or len(json_data["articles"]) == 0:
            speak("No news articles found.")
            return

        headlines = [article["title"] for article in json_data["articles"][:5]]

        for headline in headlines:
            speak(headline)

    except Exception as e:
        speak("Failed to fetch news.")


# Function to get a joke
def get_joke():
    url = "https://official-joke-api.appspot.com/random_joke"
    json_data = requests.get(url).json()
    speak(json_data["setup"])
    speak(json_data["punchline"])

# Function to fetch response from OpenAI (ChatGPT)
def chatgpt_response(query):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": query}]
        )
        answer = response["choices"][0]["message"]["content"]
        speak(answer + " from ChatGPT")
    except Exception as e:
        print(f"ChatGPT Error: {e}")
        speak("Sorry, I couldn't fetch the response from ChatGPT.")


# Function to open applications
def open_application(app_name):
    try:
        if "notepad" in app_name:
            os.system("notepad.exe")
        elif "chrome" in app_name:
            os.system("start chrome")
        elif "calculator" in app_name:
            os.system("calc.exe")
        else:
            speak("Sorry, I cannot open this application.")
    except:
        speak("Error opening application.")

# Function to close applications
def close_application(app_name):
    try:
        for process in psutil.process_iter(['pid', 'name']):
            if app_name.lower() in process.info['name'].lower():
                psutil.Process(process.info['pid']).terminate()
                return
        speak(f"Application '{app_name}' is not running.")
    except:
        speak("Error closing application.")

# Function to process commands
def process_command():
    while True:
        try:
            with sr.Microphone() as source:
                r.adjust_for_ambient_noise(source, 1.2)
                chat_window.insert(tk.END, "Listening...\n")
                chat_window.yview(tk.END)
                audio = r.listen(source)
                text = r.recognize_google(audio).lower()
                chat_window.insert(tk.END, "You: " + text + "\n")
                chat_window.yview(tk.END)

            if "exit" in text or "quit" in text or "bye" in text or "goodbye" in text or "good bye" in text:
                speak("Goodbye sir! Have a great day.")
                tk_root.quit()
            elif "time" in text:
                tell_time()
            elif "introduce yourself" in text or "who are you" in text:
                introduce()
            elif "what is your name" in text or "your name" in text:
                speak(ASSISTANT_NAME)
            elif "weather" in text:
                speak("Tell me the city name.")
                with sr.Microphone() as source:
                    audio = r.listen(source)
                    city = r.recognize_google(audio)
                get_weather(city)
            elif "news" in text:
                speak("Fetching the latest news.")
                get_news()
            elif "joke" in text or "jokes" in text:
                get_joke()
            elif "open" in text:
                app_name = text.replace("open", "").strip()
                open_application(app_name)
            elif "close" in text:
                app_name = text.replace("close", "").strip()
                close_application(app_name)
            elif any(keyword in text for keyword in ["from chatgpt", "gpt", "chat gpt"]):
                query = text.replace("from chatgpt", "").replace("gpt", "").replace("chat gpt", "").strip()
                chatgpt_response(query)
            else:
                speak("I didn't understand that. Can you please repeat?")
        except:
            query = text.replace("from chatgpt", "").strip()
            chatgpt_response(query)
            # speak("Sorry, I couldn't understand. Please try again.")

# Function to start assistant in a thread
def start_assistant():
    threading.Thread(target=process_command, daemon=True).start()

# Function to exit
def exit_app():
    speak("Goodbye sir! Have a great day.")
    tk_root.quit()

# Creating UI
tk_root = tk.Tk()
tk_root.title("Sifra")
tk_root.geometry("500x600")
tk_root.resizable(False, False)

# Chat window
chat_frame = tk.Frame(tk_root)
chat_frame.pack(pady=10)
chat_window = scrolledtext.ScrolledText(chat_frame, wrap=tk.WORD, width=60, height=20)
chat_window.pack()

# Buttons
start_button = tk.Button(tk_root, text="Start Listening", command=start_assistant, bg="green", fg="white", font=("Arial", 12))
start_button.pack(pady=10)
exit_button = tk.Button(tk_root, text="Exit", command=exit_app, bg="red", fg="white", font=("Arial", 12))
exit_button.pack()

# Greeting
speak(f"Hello sir, {wishme()} I am {ASSISTANT_NAME}, your voice assistant.")
speak("Click the Start Listening button to give a command.")

# Run UI
tk_root.mainloop()
