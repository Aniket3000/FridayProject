import pyttsx3
import datetime
import speech_recognition as sr
import wikipedia
import webbrowser
import os
import random
import smtplib
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager

engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
#print(voices[1].id)
engine.setProperty('voice',voices[1].id)

def speak(audio):
    engine.say(audio)
    engine.runAndWait()

def wishMe():
    hour = int(datetime.datetime.now().hour)
    if hour >= 0 and hour < 12:
        speak("Good Morning!")

    elif hour >=12 and hour < 18:
        speak("Good Afternoon!")

    else:
        speak("Good Evening")

    speak("Friday Reporting Sir, how can I help you Sir??")

def whatsapp():
    driver = webdriver.Chrome(ChromeDriverManager().install())
    driver.get('https://web.whatsapp.com/')
    # wait = WebDriverWait(driver, 600)


    print("To whom do you want to send the message boss?")
    speak("To whom do you want to send the message boss?")
    to = takeCommand()
    print("And the message")
    speak("And what message?")
    msg = takeCommand()
    
    
    print('Enter anything after scanning QR Code')
    speak("Enter anything after scanning QR Code")
    
    to = to.title()
    user = driver.find_element_by_xpath('//span[@title = "{}"]'.format(to))
    user.click()

    msg_box = driver.find_element_by_class_name('_3uMse')
    msg_box.send_keys(msg)
    button = driver.find_element_by_class_name('_1U1xa')
    button.click()
    speak("Message sent boss!!")


def takeCommand():
    # It takes microphone input from the user and returns string output

    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 1
        audio = r.listen(source)

    try:
        print("Recognizing...")
        query = r.recognize_google(audio, language='en-in')
        print(f"User said: {query}\n")

    except Exception as e:
        # print(e)
        print("Say that again please...")
        speak("Sorry Boss, couldn't get it..")
        takeCommand()
        return "None"
    return query

def sendEmail(to, content):
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.login('youremail@gmail.com','your-password')
    server.sendmail('youremail@gmail.com',to,content)
    server.close()
    
if __name__ == "__main__":
    wishMe()
    #speak("Hello Honey")
    while(True):
        query = takeCommand().lower()
        if 'friday' in query:
            #Logic for executing tasks based on query
            if 'wikipedia' in query:
                speak("Searching in wikipedia....")
                query = query.replace("wikipedia","")
                results = wikipedia.summary(query, sentences = 2)
                print(results)
                speak("According to Wikipedia")
                speak(results)

            elif 'open youtube' in query:
                webbrowser.open("youtube.com")

            elif 'open google' in query:
                webbrowser.open("google.com")
            
            elif 'search' in query:
                word_list = query.split()
                word = []
                for words in word_list:
                    if ((words != 'friday') and (words != 'search') and (words != 'what') and (words != 'in') and (words != 'is') and (words != 'and') and (words != 'or')):
                        word.append(words)
                print(*word, sep = " ")
                url = "https://www.google.com.tr/search?q={}".format(' '.join(word))
                chrome_browser = webbrowser.get("C:/Program Files (x86)/Google/Chrome/Application/chrome.exe %s")
                chrome_browser.open_new_tab(url)
        
            elif 'open facebook' in query:
                webbrowser.open("facebook.com")

            elif 'open coursera' in query:
                webbrowser.open("coursera.com")

            elif 'play some music' in query:
                music_dir = 'F:\\Favourites'
                songs = os.listdir(music_dir)
                print(songs)
                a = random.randint(0,len(songs))
                os.startfile(os.path.join(music_dir, songs[a]))

            elif 'the time' in query:
                strTime = datetime.datetime.now().strftime("%H:%M:%S")
                speak(f"Sir, The time is {strTime}")

            elif 'open vs code' in query:
                codePath = "C:\\Users\\Aniket\\AppData\\Local\\Programs\\Microsoft VS Code\\Code.exe"
                os.startfile(codePath)

            elif 'send message on whatsapp' in query:
                try:
                    whatsapp()
                except Exception as e:
                    print(e)
                    speak("Sorry boss, not able to send the message at the moment.")

            elif 'send email' in query:
                try:
                    speak("What do you want to send boss?")
                    content = takeCommand()
                    to = "nyp.aniket@gmail.com"
                    sendEmail(to, content)
                    speak("Email Sent boss, What next?")
                except Exception as e:
                    print(e)
                    speak("Sorry boss, not able to send the email at the moment.")

            elif 'quit' in query:
                print("Signing off boss...")
                speak("Signing off boss...")
                break
            else:
                speak(query)

        else:
            speak("Sorry well i am friday you have to say that..")
