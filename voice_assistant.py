import pyttsx3   
import speech_recognition as sr  
import datetime
import wikipedia
import webbrowser
import os
import random
import smtplib
import warnings
import operator
from gtts import gTTS
import calendar

# ignore any warnings
warnings.filterwarnings('ignore')

engine=pyttsx3.init('sapi5')
voices=engine.getProperty('voices')
engine.setProperty('voice',voices[0].id)

def speak(audio):
    engine.say(audio)
    engine.runAndWait()

# function to get current date
def getDate():
    now=datetime.datetime.now()
    my_date=datetime.datetime.today()
    weekday=calendar.day_name[my_date.weekday()]
    monthNum=now.month
    dayNum=now.day
    month_names=['January','February','March','April','May','June','July','August','September','October','November','December']

    ordinalNumbers=['1st','2nd','3rd','4th','5th','6th','7th','8th','9th','10th','11th','12th','13th','14th','15th','16th','17th','18th','19th','20th','21st','22nd','23rd','24th','25th','26th','27th','28th','29th','30th','31st']
    return 'Today is '+weekday+' '+month_names[monthNum-1]+' the '+ ordinalNumbers[dayNum-1]+'.'


def wishMe():
    hour=int(datetime.datetime.now().hour)
    if hour>=0 and hour<12:
        speak("Good Morning!")
    elif hour>=12 and hour<18:
        speak("Good Afternoon!")
    else:
        speak("Good Evening!")
    speak("I am Jarvis. Please tell me How may i help u")

def takeCommand():
    # It takes microphone input from user and return string output

    r=sr.Recognizer()   #Recognizer class to recognize audio
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold=1    # seconds of non-speaking audio before a phrase is considered complete

        audio=r.listen(source)
    query=''
    try:
        print("Recognizing...")
        query=r.recognize_google(audio,language="en-in")   #using google speech recognition
        print(f"You said : {query}\n")
    except sr.UnknownValueError:
        print('Google Speech Recognition could not understand the audio, unknown error')
        speak('Google Speech Recognition could not understand the audio, unknown error')
    except sr.RequestError as e:
        print(f'Request results from Google Speech Recognition service error {e}')
        speak(f'Request results from Google Speech Recognition service error {e}')

    return query   

def sendEmail(to,content):
    server=smtplib.SMTP('smtp.gmail.com',587)
    server.ehlo()              #identify to server
    server.starttls()          #encrypt session
    server.login('sender email','sender password')
    server.sendmail('sender email',to,content)
    server.close()


def get_operator_fn(op):
    return {
        '+' : operator.add,
        '-' : operator.sub,
        'x' : operator.mul,
        'divide' :operator.__truediv__,
        'mod' : operator.mod,
        '^' : operator.xor,
        }[op]

def eval_binary_expr(op1, oper, op2):
    op1,op2 = int(op1), int(op2)
    return get_operator_fn(oper)(op1, op2)

if __name__=="__main__":
    wishMe()
    while True:
        query=takeCommand().lower()
        if query=="":
            continue
        #logic for executing tasks based on query
        if 'wikipedia' in query:
            speak('Searching Wikipedia...')
            query=query.replace("wikipedia","")
            results=wikipedia.summary(query,sentences=2)
            speak("According to Wikipedia")
            print(results)
            speak(results)

        elif 'open youtube' in query:
            speak('Opening Youtube...')
            webbrowser.open("youtube.com")
        
        elif 'open google' in query:
            speak('Opening Google...')
            webbrowser.open("google.com")

        elif 'open stackoverflow' in query:
            speak('Opening Stackoverflow...')
            webbrowser.open("stackoverflow.com")

        elif 'play music' in query:
            speak('Playing music...')
            music_dir="C:\\Users\\Dell\\Desktop\\New folder (2)"     # music directory path
            songs=os.listdir(music_dir)
            print(songs)
            os.startfile(os.path.join(music_dir,random.choice(songs)))
        
        elif 'time' in query:
            strTime=datetime.datetime.now().strftime("%H:%M:%S")
            print(strTime)
            speak(f"the time is {strTime}")

        elif 'date' in query:
            date=getDate()
            print(date)
            speak(date)

        elif 'open code' in query:
            codePath="C:\\Users\\Dell\\AppData\\Local\\Programs\\Microsoft VS Code\\Code.exe"     # code editor path 
            os.startfile(codePath)
        
        elif 'send email' in query:
            try:
                speak("what should i say?")
                content=takeCommand()
                to="receiver email"
                sendEmail(to,content)
                speak("Email has been sent")
            except Exception as e:
                print(e)
                speak("Sorry i am not able to send this email")
            
        elif 'calculate' in query:
            query=query.replace("calculate","")
            try:
                ans=eval_binary_expr(*(query.split()))
                print(ans)
                speak(ans)
            except Exception as e:
                print("Google Speech Recognition could not understand the audio")
                speak("Google Speech Recognition could not understand the audio")
        

        elif 'keep quiet' in query or 'shut up' in query:
            speak('ok, have a nice day')
            break

        else:
            webbrowser.open("http://www.google.com/search?btnG=1&q=%s"% query)
