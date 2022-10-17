import datetime
import requests
from config import open_weather_token
from kivy.app import App
from kivy.config import Config
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.floatlayout import FloatLayout


Config.set('graphics','width','500')
Config.set('graphics','height','550')

description = {
    "Clear": "Ясно",
    "Clouds": "Хмарно",
    "Rain": "Дощ",
    "Drizzle": "Дощ",
    "Thunderstorm": "Гроза",
    "Snow": "Сніг",
    "Mist": "Туман"
}

def get_weather(location, open_weather_token):
    try:
        r = requests.get(
            f"https://api.openweathermap.org/data/2.5/weather?q={location}&appid={open_weather_token}&units=metric"
        )
        data = r.json()

        location = data['name']
        temperature = data['main']['temp']
        humidity = data['main']['humidity']
        pressure = data['main']['pressure']
        wind = data['wind']['speed']
        sunrise = datetime.datetime.fromtimestamp(data['sys']['sunrise'])
        sunset = datetime.datetime.fromtimestamp(data['sys']['sunset'])
        weather_description = data['weather'][0]['main']
        if weather_description in description:
            wd = description[weather_description]
        else:
            wd = "Подивись у вікно"

        global weather
        weather = (f"***{datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}***\n"
                   f"Погода в населеному пункті {location}: {wd}\n"
                   f"Температура повітря: {temperature}°C\n"
                   f"Вологість повітря: {humidity}%\n"
                   f"Атмосферний тиск: {pressure} гПа\n"
                   f"Швидкість вітру: {wind} м/с\n"
                   f"Схід сонця: {sunrise}\n"
                   f"Захід сонця: {sunset}\n"
                   f"Хорошого дня!)"
                   )

    except:
        print("Перевірте назву населеного пункту")


class MyFloat(FloatLayout):
    def __init__(self, **kwargs):
        super(MyFloat, self).__init__(**kwargs)

        self.request = Label(text="Введіть населений пункт: ", font_size=20, size_hint=(0.45, 0.15), pos=(20, 435))
        self.add_widget(self.request)

        self.location = TextInput(multiline=False, font_size=20, size_hint=(0.45, 0.10), pos=(265, 441))
        self.add_widget(self.location)

        self.submit = Button(text="Submit", size_hint=(0.3, 0.1), pos=(320, 380))
        self.submit.bind(on_press=self.pressed)
        self.add_widget(self.submit)

        self.display = Label(font_size=20, size_hint=(0.75, 0.55), pos=(60, 70))
        self.add_widget(self.display)

    def pressed(self, instance):
        location = self.location.text
        get_weather(location, open_weather_token)
        try:
            self.display.color = (1, 1, 1, 1)
            self.display.text = weather
        except:
            self.display.color = (1, 0, 0, 1)
            self.display.text = "Перевірте назву населеного пункту"

class WeatherApp(App):
    def build(self):
        return MyFloat()

if __name__ == "__main__":
    WeatherApp().run()
