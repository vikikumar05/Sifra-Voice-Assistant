from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivymd.app import MDApp
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.scrollview import MDScrollView
from kivymd.uix.label import MDLabel
import threading
import speech_recognition as sr
import pyttsx3
import datetime
import os
import requests
import openai
import psutil
import json

# Initialize speech engine
engine = pyttsx3.init()
engine.setProperty('rate', 140)
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)

# Initialize speech recognizer
recognizer = sr.Recognizer()

# Assistant Name
ASSISTANT_NAME = "Sifra"

# OpenAI API Key (Replace with your API key)
OPENAI_API_KEY = "###################################"
openai.api_key = OPENAI_API_KEY

KV = """
ScreenManager:
    MainScreen:

<MainScreen>:
    name: 'main'
    MDBoxLayout:
        orientation: 'vertical'
        MDScrollView:
            MDBoxLayout:
                id: chat_window
                orientation: 'vertical'
                size_hint_y: None
                height: self.minimum_height
        MDRaisedButton:
            text: 'Start Listening'
            pos_hint: {'center_x': 0.5}
            on_release: app.start_listening()
        MDRaisedButton:
            text: 'Exit'
            pos_hint: {'center_x': 0.5}
            md_bg_color: 1, 0, 0, 1
            on_release: app.stop_app()
"""

class MainScreen(Screen):
    pass

class VoiceAssistantApp(MDApp):
    def build(self):
        self.sm = ScreenManager()
        self.sm.add_widget(MainScreen(name='main'))
        return self.sm

    def update_chat(self, sender, message):
        chat_box = self.sm.get_screen('main').ids.chat_window
        chat_box.add_widget(MDLabel(text=f"{sender}: {message}", size_hint_y=None, height=40))

    def speak(self, text):
        self.update_chat("Sifra", text)
        engine.say(text)
        engine.runAndWait()

    def listen_command(self):
        with sr.Microphone() as source:
            recognizer.adjust_for_ambient_noise(source)
            self.update_chat("Sifra", "Listening...")
            audio = recognizer.listen(source)
        try:
            command = recognizer.recognize_google(audio).lower()
            self.update_chat("You", command)
            self.process_command(command)
        except sr.UnknownValueError:
            self.speak("Sorry, I didn't catch that.")

    def start_listening(self):
        threading.Thread(target=self.listen_command, daemon=True).start()

    def process_command(self, command):
        if "exit" in command:
            self.speak("Goodbye!")
            self.stop()
        elif "time" in command:
            now = datetime.datetime.now().strftime("%I:%M %p")
            self.speak(f"The time is {now}")
        elif "introduce" in command:
            self.speak(f"Hello, I am {ASSISTANT_NAME}, your voice assistant.")
        elif "weather" in command:
            self.get_weather("your_city")
        elif "news" in command:
            self.get_news()
        elif "joke" in command:
            self.get_joke()
        elif "open" in command:
            self.open_application(command.replace("open", "").strip())
        elif "close" in command:
            self.close_application(command.replace("close", "").strip())
        elif "gpt" in command:
            self.chatgpt_response(command.replace("gpt", "").strip())
        else:
            self.speak("I didn't understand that.")

    def get_weather(self, city):
        API_KEY = "##############################"
        url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
        try:
            response = requests.get(url).json()
            if response["cod"] != 200:
                self.speak("Could not fetch weather details.")
                return
            temp = response["main"]["temp"]
            description = response["weather"][0]["description"]
            self.speak(f"The temperature in {city} is {temp}°C with {description}.")
        except:
            self.speak("Error fetching weather.")

    def get_news(self):
        API_KEY = "###################################"
        url = f"https://newsapi.org/v2/top-headlines?country=in&apiKey={API_KEY}"
        try:
            response = requests.get(url).json()
            articles = response.get("articles", [])[:5]
            if not articles:
                self.speak("No news found.")
                return
            for article in articles:
                self.speak(article["title"])
        except:
            self.speak("Failed to fetch news.")

    def get_joke(self):
        url = "https://official-joke-api.appspot.com/random_joke"
        try:
            joke = requests.get(url).json()
            self.speak(joke["setup"])
            self.speak(joke["punchline"])
        except:
            self.speak("Couldn't fetch a joke.")

    def chatgpt_response(self, query):
        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": query}]
            )
            answer = response["choices"][0]["message"]["content"]
            self.speak(answer)
        except:
            self.speak("Could not fetch response from ChatGPT.")

    def open_application(self, app_name):
        if "notepad" in app_name:
            os.system("notepad.exe")
        elif "chrome" in app_name:
            os.system("start chrome")
        elif "calculator" in app_name:
            os.system("calc.exe")
        else:
            self.speak("Cannot open this application.")

    def close_application(self, app_name):
        for process in psutil.process_iter(['pid', 'name']):
            if app_name.lower() in process.info['name'].lower():
                psutil.Process(process.info['pid']).terminate()
                return
        self.speak(f"Application '{app_name}' is not running.")

    def stop_app(self):
        self.speak("Goodbye!")
        self.stop()

if __name__ == "__main__":
    VoiceAssistantApp().run()
