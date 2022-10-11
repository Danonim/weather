import requests
import datetime
from pprint import pprint
from config import open_weather_token


def get_weather(location, open_weather_token):
    emoji = {
        "Clear": "Ясно \U00002600",
        "Clouds": "Хмарно \U00002601",
        "Rain": "Дощ \U00002614",
        "Drizzle": "Дощ \U00002614",
        "Thunderstorm": "Гроза \U000026A1",
        "Snow": "Сніг \U0001F328",
        "Mist": "Туман \U0001F32B"
    }

    try:
        r = requests.get(
            f"https://api.openweathermap.org/data/2.5/weather?q={location}&appid={open_weather_token}&units=metric"
        )
        data = r.json()
        # pprint(data)

        location = data['name']
        temperature = data['main']['temp']
        humidity = data['main']['humidity']
        pressure = data['main']['pressure']
        wind = data['wind']['speed']
        sunrise = datetime.datetime.fromtimestamp(data['sys']['sunrise'])
        sunset = datetime.datetime.fromtimestamp(data['sys']['sunset'])
        weather_description = data['weather'][0]['main']
        if weather_description in emoji:
            wd = emoji[weather_description]
        else:
            wd = "Подивись у вікно \U0001F609"

        print(f"***{datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}***\n"
              f"Погода в населеному пункті {location}: {wd}\n"
              f"Температура повітря: {temperature}°C\n"
              f"Вологість повітря: {humidity}%\n"
              f"Атмосферний тиск: {pressure} мм рт. ст.\n"
              f"Швидкість вітру: {wind} м/с\n"
              f"Схід сонця: {sunrise}\n"
              f"Захід сонця: {sunset}\n"
              f"Хорошого дня!)"
              )

    except:
        print("Перевірте назву населеного пункту")

def main():
    location = input("Введіть населений пункт: ")
    get_weather(location, open_weather_token)

if __name__ == '__main__':
    main()
