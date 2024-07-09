import requests
import pyttsx3
import speech_recognition as sr
from decouple import config
from datetime import datetime
from random import choice
from utils import opening_text
from pprint import pprint
import subprocess as sp
import requests
import wikipedia
import pywhatkit as kit
import os
from email.message import EmailMessage
import smtplib
from decouple import config
import webbrowser
import pyautogui


USERNAME = config('USER')
BOTNAME = config('BOTNAME')


engine = pyttsx3.init('sapi5')


engine.setProperty('rate', 190)

engine.setProperty('volume', 1.0)


voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)



def speak(text):
    engine.say(text)
    engine.runAndWait()


def greet_user():
    
    hour = datetime.now().hour
    if (hour >= 6) and (hour < 12):
        print(f"Good Morning {USERNAME}")
        speak(f"Good Morning {USERNAME}")
        
    elif (hour >= 12) and (hour < 16):
        print(f"Good afternoon {USERNAME}")
        speak(f"Good afternoon {USERNAME}")
        
    elif (hour >= 16) and (hour < 19):
        print(f"Good Evening {USERNAME}")
        speak(f"Good Evening {USERNAME}")
    print(f"I am {BOTNAME}. How may I assist you?")    
    speak(f"I am {BOTNAME}. How may I assist you?")
    


paths = {
    'notepad': "C:\\Program Files\\Notepad++\\notepad++.exe",
    'discord': "C:\\Users\\ashut\\AppData\\Local\\Discord\\app-1.0.9003\\Discord.exe",
    'calculator': "C:\\Windows\\System32\\calc.exe"
}


def open_notepad():
    webbrowser.open("https://onlinenotepad.org/notepad")

def open_discord():
    os.startfile(paths['discord'])


def open_cmd():
    os.system('start cmd')


def open_camera():
    sp.run('start microsoft.windows.camera:', shell=True)


def open_calculator():
    sp.Popen(paths['calculator'])



NEWS_API_KEY = config("NEWS_API_KEY")
# OPENWEATHER_APP_ID = config("OPENWEATHER_APP_ID")
# TMDB_API_KEY = config("TMDB_API_KEY")
EMAIL = config("EMAIL")
PASSWORD = config("PASSWORD")


def type_message():
    speak("Please tell me what should i write.")
    print("Please tell me what should i write.")
    while True:
        typequery=take_user_input()

        if typequery=='exit typing':
            break
        else:
            pyautogui.write(typequery)



def find_my_ip():
    ip_address = requests.get('https://api64.ipify.org?format=json').json()
    return ip_address["ip"]


def search_on_wikipedia(query):
    results = wikipedia.summary(query, sentences=2)
    return results


def play_on_youtube(video):
    kit.playonyt(video)


def search_on_google(query):
    kit.search(query)


def send_whatsapp_message(number, message):
    kit.sendwhatmsg_instantly(f"+91{number}", message)


def send_email(receiver_address, subject, message):
    try:
        email = EmailMessage()
        email['To'] = receiver_address
        email["Subject"] = subject
        email['From'] = EMAIL
        email.set_content(message)
        s = smtplib.SMTP("smtp.gmail.com", 587)
        s.starttls()
        s.login(EMAIL, PASSWORD)
        s.send_message(email)
        s.close()
        return True
    except Exception as e:
        print(e)
        return False


def get_latest_news():
    news_headlines = []
    res = requests.get(
        f"https://newsapi.org/v2/top-headlines?country=in&apiKey={NEWS_API_KEY}&category=general").json()
    articles = res["articles"]
    for article in articles:
        news_headlines.append(article["title"])
    return news_headlines[:5]


def get_weather_report(city):
    # res = requests.get(
    #     f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={OPENWEATHER_APP_ID}&units=metric").json()
    
    res={
    "coord": {
        "lon": 85,
        "lat": 24.7833
    },
    "weather": [
        {
            "id": 721,
            "main": "Haze",
            "description": "haze",
            "icon": "50d"
        }
    ],
    "base": "stations",
    "main": {
        "temp": 26.95,
        "feels_like": 26.64,
        "temp_min": 26.95,
        "temp_max": 26.95,
        "pressure": 1011,
        "humidity": 36
    },
    "visibility": 3000,
    "wind": {
        "speed": 2.57,
        "deg": 310
    },
    "clouds": {
        "all": 57
    },
    "dt": 1637227634,
    "sys": {
        "type": 1,
        "id": 9115,
        "country": "IN",
        "sunrise": 1637195904,
        "sunset": 1637235130
    },
    "timezone": 19800,
    "id": 1271439,
    "name": "Gaya",
    "cod": 200
}
    weather = res["weather"][0]["main"]
    temperature = res["main"]["temp"]
    feels_like = res["main"]["feels_like"]
    return weather, f"{temperature}℃", f"{feels_like}℃"


# def get_trending_movies():
#     trending_movies = []
#     res = requests.get(
#         f"https://api.themoviedb.org/3/trending/movie/day?api_key={TMDB_API_KEY}").json()
#     results = res["results"]
#     for r in results:
#         trending_movies.append(r["original_title"])
#     return trending_movies[:5]


def get_random_joke():
    headers = {
        'Accept': 'application/json'
    }
    res = requests.get("https://icanhazdadjoke.com/", headers=headers).json()
    return res["joke"]


def get_random_advice():
    res = requests.get("https://api.adviceslip.com/advice").json()
    return res['slip']['advice']



def take_user_input():
    
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print('Listening....')
        r.pause_threshold = 1
        r.adjust_for_ambient_noise(source, duration=1)
        audio = r.listen(source)

    try:
        
        print('Recognizing...')
       
        query = r.recognize_google(audio, language='en-in')
        print("user said: ", query)
        if not 'exit' in query or 'stop' in query:
            print(choice(opening_text))
            speak(choice(opening_text))
        else:
            hour = datetime.now().hour
            if hour >= 21 and hour < 6:
                print("Good night sir, take care!")
                speak("Good night sir, take care!")
            else:
                print('Have a good day sir!')
                speak('Have a good day sir!')
            exit()
    except Exception:
        print('Sorry, I could not understand. Could you please say that again?')
        speak('Sorry, I could not understand. Could you please say that again?')
        query = 'None'
    return query


if __name__ == '__main__':
    greet_user()
    while True:
        query = take_user_input().lower()

        if 'open notepad' in query:
            open_notepad()

        elif 'open discord' in query:
            open_discord()

        elif 'open command prompt' in query or 'open cmd' in query:
            open_cmd()

        elif 'open camera' in query:
            open_camera()

        elif 'open calculator' in query:
            open_calculator()

        elif 'ip address' in query:
            ip_address = find_my_ip()
            print(f'Your IP Address is {ip_address}.\n For your convenience, I am printing it on the screen sir.')
            speak(f'Your IP Address is {ip_address}.\n For your convenience, I am printing it on the screen sir.')
            
            print(f'Your IP Address is {ip_address}')

        elif 'wikipedia' in query:
            print('What do you want to search on Wikipedia, sir?')
            speak('What do you want to search on Wikipedia, sir?')
            search_query = take_user_input().lower()
            results = search_on_wikipedia(search_query)
            print(f"According to Wikipedia, {results}")
            speak(f"According to Wikipedia, {results}")
            print("For your convenience, I am printing it on the screen sir.")
            speak("For your convenience, I am printing it on the screen sir.")
            print(results)
            speak(results)

        elif 'youtube' in query:
            print('What do you want to play on Youtube, sir?')
            speak('What do you want to play on Youtube, sir?')
            video = take_user_input().lower()
            play_on_youtube(video)

        elif 'search on google' in query or 'search' in query:
            print('What do you want to search on Google, sir?')
            speak('What do you want to search on Google, sir?')
            query = take_user_input().lower()
            search_on_google(query)

        elif "send whatsapp message" in query or "send message" in query or "message whatsapp" in query:
            print(
                'On what number should I send the message sir? Please enter in the console: ')
            speak(
                'On what number should I send the message sir? Please enter in the console: ')
            number = input("Enter the number: ")
            print("What is the message sir?")
            speak("What is the message sir?")
            message = take_user_input().lower()
            send_whatsapp_message(number, message)
            speak("I've sent the message sir.")

        elif "send an email" in query or "send email" in query or "send mail" in query or "send a mail" in query:
            speak("On what email address do I send sir? Please enter in the console: ")
            receiver_address = input("Enter email address: ")
            speak("What should be the subject sir?")
            subject = take_user_input().capitalize()
            speak("What is the message sir?")
            message = take_user_input().capitalize()
            if send_email(receiver_address, subject, message):
                speak("I've sent the email sir.")
            else:
                speak("Something went wrong while I was sending the mail. Please check the error logs sir.")

        elif 'joke' in query:
            speak(f"Hope you like this one sir")
            joke = get_random_joke()
            speak(joke)
            speak("For your convenience, I am printing it on the screen sir.")
            pprint(joke)

        elif "advice" in query:
            print(f"Here's an advice for you, sir")
            speak(f"Here's an advice for you, sir")
            advice = get_random_advice()
            print(advice)
            print("For your convenience, I am printing it on the screen sir.")
            speak(advice)
            speak("For your convenience, I am printing it on the screen sir.")
            pprint(advice)

        # elif "trending movies" in query:
        #     speak(f"Some of the trending movies are: {get_trending_movies()}")
        #     speak("For your convenience, I am printing it on the screen sir.")
        #     print(*get_trending_movies(), sep='\n')

        elif 'news' in query:
            print(f"I'm reading out the latest news headlines, sir")
            speak(f"I'm reading out the latest news headlines, sir")
            print(get_latest_news())
            speak(get_latest_news())
            print("For your convenience, I am printing it on the screen sir.")
            speak("For your convenience, I am printing it on the screen sir.")
            print(*get_latest_news(), sep='\n')
            speak(*get_latest_news())

        elif 'weather' in query:
            ip_address = find_my_ip()
            city = requests.get(f"https://ipapi.co/{ip_address}/city/").text
            speak(f"Getting weather report for your city {city}")
            print(f"Getting weather report for your city {city}")
            weather, temperature, feels_like = get_weather_report(city)
            speak(f"The current temperature is {temperature}, but it feels like {feels_like}")
            speak(f"Also, the weather report talks about {weather}")
            speak("For your convenience, I am printing it on the screen sir.")
            print(f"Description: {weather}\nTemperature: {temperature}\nFeels like: {feels_like}")

        elif 'type' in query or 'type message' in query:
            type_message()   