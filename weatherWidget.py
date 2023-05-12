# importing required librarie
import sys

from PyQt6 import QtCore
from PyQt6.QtWidgets import QApplication, QWidget, QHBoxLayout
from PyQt6.QtWidgets import QVBoxLayout, QLabel
from PyQt6.QtGui import QFont
from PyQt6.QtCore import QTimer, QTime, Qt


class MyWeather(QWidget):

    def __init__(self):
        super().__init__()

        self.label = QLabel()
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label.setWordWrap(True)

        layout = QHBoxLayout()
        layout.addWidget(self.label)

        self.setLayout(layout)

        self.get_weather_string()

    def get_weather_string(self):
        import requests
        s_city = "Anapa,RU"
        city_id = 0
        appid = "4313b9e8ad54b793de19b8ade568bdcc"

        try:
            res = requests.get("http://api.openweathermap.org/data/2.5/find",
                               params={'q': s_city, 'type': 'like', 'units': 'metric', 'APPID': appid})
            data = res.json()
            cities = ["{} ({})".format(d['name'], d['sys']['country'])
                      for d in data['list']]
            print("city:", cities)
            city_id = data['list'][0]['id']
            # print('city_id=', city_id)
        except Exception as e:
            # print("Exception (find):", e)
            pass

        try:
            res = requests.get("http://api.openweathermap.org/data/2.5/weather",
                               params={'id': city_id, 'units': 'metric', 'lang': 'ru', 'APPID': appid})
            data = res.json()
            print("conditions:", data['weather'][0]['description'])
            print("temp:", data['main']['temp'])
            print("temp_min:", data['main']['temp_min'])
            print("temp_max:", data['main']['temp_max'])
        except Exception as e:
            print("Exception (weather):", e)
            pass

        if 'data' in locals():
            # return '{} {}'.format(data['weather'][0]['description'], data['main']['temp'])
            # self.label.setText('{}\n {} {}{}'.format(cities[0], data['weather'][0]['description'], data['main']['temp'], '°'))
            self.label.setText('{}\n {}\n {}{}'.format('Анапа:', data['weather'][0]['description'], data['main']['temp'], '°'))
        else:
            # return 'ᓚᘏᗢ'
            self.label.setText('ᓚᘏᗢ')