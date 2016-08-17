import pyowm
import keys
import sqlite3
import directionutils
import feedparser
# connect and create sqlite tables
conn = sqlite3.connect('sth.db')
cur = conn.cursor()
import datetime


def play_greeting():
    print(' Annoucements - play greeting')
    return 'yes, kakka Peehu'


def play_trivia():
    return "A trivia, An ant can lift thirty times it's body weight"


def play_story():
    return 'this is a story'


def play_im_fine():
    return 'hey, thanks for asking, i am fine, how are you doing'



def play_weather_info():
    owm = pyowm.OWM(keys.pyowm_key)  # You MUST provide a valid API key

    # You have a pro subscription? Use:
    # owm = pyowm.OWM(API_key='your-API-key', subscription_type='pro')

    # Will it be sunny tomorrow at this time in Milan (Italy) ?
    forecast = owm.daily_forecast("Pune,India")
    tomorrow = pyowm.timeutils.tomorrow()
    # forecast.will_be_sunny_at(tomorrow)  # Always True in Italy, right? ;-)

    # Search for current weather in London (UK)
    observation = owm.weather_at_place('Pune,India')
    w = observation.get_weather()
    # print(w)  # <Weather - reference time=2013-12-18 09:20,
    # status=Clouds>

    # Weather details
    wind = w.get_wind()  # {'speed': 4.6, 'deg': 330}
    humidity = w.get_humidity()  # 87
    temp = w.get_temperature('celsius')  # {'temp_max': 10.5, 'temp': 9.7, 'temp_min': 9.0}

    #print(wind,humidity,temp)

    # Search current weather observations in the surroundings of
    # lat=22.57W, lon=43.12S (Rio de Janeiro, BR)
    # observation_list = owm.weather_around_coords(-22.57, -43.12)

    instructions = ""
    if w.get_status() == "Rain":
        instructions = ", please carry an umbrella or raincoat"

    return "Weather Update For today. The weather status for today is, " + w.get_status() + instructions


def play_traffic_info(to_location):
     duration_in_traffic =  divmod( directionutils.get_traffic_data_for_today('ranjan')[0]['duration_in_traffic'], 60)
     #avg_duration_in_traffic = directionutils.get_avg_duration('ranjan','to_office')
     #print(duration_in_traffic)
     if duration_in_traffic[0] > 45:
         return "Traffic update for Today, duration to office right now is too high at {0} minutes".format(duration_in_traffic[0])
     return "Traffic update for Today, duration to office right now is {0} minutes".format(duration_in_traffic[0])


def play_top_news():
    d = feedparser.parse('http://timesofindia.indiatimes.com/rssfeedstopstories.cms')
    news = []
    for i in d.entries:
        news.append(i.title)

    return ', '.join(news)
if __name__ == "__main__":
    # print(get_weather_info())
    # print(get_traffic_info('office'))
    print(play_top_news())