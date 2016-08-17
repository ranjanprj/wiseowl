import json
import time as t
from datetime import datetime,time
from multiprocessing import Process
from random import randint

import announcements
import directionutils as du
import owlspeak
import listenowl
from bottle import route, run, template, request, post, get
from subprocess import Popen

from gpiozero import Button
from signal import pause

def recognize_voice():
    listenowl.speak_spoken_words()


def voice_jobs():
    """
        do voice recognition
    """
    print("Button is pressed")
    button = Button(2)
    button.when_pressed = listenowl.speak_spoken_words
    pause()



def announcements_jobs():
    annoucements = 0
    while True:
        print("Running Annoucements Job")
        """
            do morning announcements
        """
        print("Morning announcements running")
        now = datetime.now()
        while annoucements < 4:
            if now.time() >= time(8, 00):
                annoucements += 1
                # weather info
                weather_info = announcements.play_weather_info()
                owlspeak.owl_speak(weather_info)
                t.sleep(2)
                owlspeak.owl_speak(weather_info)
                t.sleep(2)
                # traffic info
                duration_in_traffic = announcements.play_traffic_info('to_office')
                owlspeak.owl_speak(duration_in_traffic)
                t.sleep(2)
                owlspeak.owl_speak(duration_in_traffic)

                # news
                t.sleep(4)
                news = announcements.play_top_news()
                owlspeak.owl_speak(news)
                t.sleep(60*15)


def traffic_job():
    while True:
        print("Running Traffic Job")

        """
            collect traffic data
        """
        sleep_time = randint(15,20)
        t.sleep(sleep_time * 60)
        # t.sleep(10)
        print("Traffic Job Running")
        du.save_traffic_data()


@route('/register')
def index():
    return template("""
        <form method='POST' action='save_user'>
            Name/Token : <input type='text' name ='user_name'/>
            Home Addr : <textarea name='home_address' ></textarea>
            <input type="submit" value="Submit">
        </form>
    """)

@post('/save_user')
def index():
    user_name = request.forms.get('user_name')
    home_address = request.forms.get('home_address')
    du.save_user_data(user_name,home_address)
    return 'You data is saved, <a href="/login">Login using your user name</a>'


@route('/login')
def index():
    return template("""
        <form method='POST' action='show_traffic'>
            User Name/Token : <input type='text' name ='user_name'/>
            <input type="submit" value="Submit">
        </form>
    """)


@post('/show_traffic')
def index():
    user_name = request.forms.get('user_name')
    print(user_name)
    traffic_data = json.dumps(du.get_traffic_data(user_name))
    print(traffic_data)
    return template("""
       Traffic data %s
    """ % str(traffic_data))

@get('/plot/<user_name>/<direction>')
def index(user_name,direction):
    get_avg = du.get_avg_duration(user_name,direction)
    plot = du.plot_bar_chart(get_avg)
    return template("""
       %s
    """ % str(plot))


def init_mary_tts():
    Popen(["sh","~/Downloads/"])
def main():
    print("main method")
    init_mary_tts()
    print("starting job")
    traffic_processor = Process(target=traffic_job)
    # my_processor.daemon = True
    traffic_processor.start()
    # my_processor.join()

    voice_processor = Process(target=voice_jobs)
    voice_processor.start()
    annoucements_processor = Process(target=announcements_jobs)
    annoucements_processor.start()

    run(host='0.0.0.0', port=8080)


if __name__ == '__main__':
    main()

