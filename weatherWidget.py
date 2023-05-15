# importing required librarie
import sys
from typing import Callable, io

import requests

from PyQt6 import QtCore
from PyQt6.QtWidgets import QApplication, QWidget, QHBoxLayout, QScrollArea
from PyQt6.QtWidgets import QVBoxLayout, QLabel
from PyQt6.QtGui import QFont
from PyQt6.QtCore import QTimer, QTime, Qt, QPoint


class WeatherFordaysItems(QWidget):

    def __init__(self, date, time, temp, comment):
        super().__init__()

        self.date = date
        self.time = time
        self.temp = temp
        self.comment = comment

        date_label = QLabel(self.date)
        time_label = QLabel(self.time)
        temp_label = QLabel(self.temp)
        comment_label = QLabel(self.comment)

        layout = QHBoxLayout()

        layout.addWidget(date_label)
        layout.addWidget(time_label)
        layout.addWidget(temp_label)
        layout.addWidget(comment_label)

        self.setLayout(layout)


class WeatherForDaysWidget(QWidget):

    def __init__(self, get_contetn: Callable[[], str]):
        super().__init__()
        self.setWindowFlags(QtCore.Qt.WindowType.FramelessWindowHint)
        self.resize(500, 100)

        title = QLabel('Прогноз на 5 дней:')
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)

        layout = QVBoxLayout()

        layout.addWidget(title)

        text = get_contetn()

        # content = QScrollArea()
        content = QLabel(text)

        layout.addWidget(content)

        self.setLayout(layout)

    def keyPressEvent(self, event):
        # Did the user press the Escape key?
        if event.key() == Qt.Key.Key_Escape:  # QtCore.Qt.Key_Escape is a value that equates to what the operating system passes to python from the keyboard when the escape key is pressed.
            # Yes: Close the window
            self.close()
        # No:  Do nothing.

    def mousePressEvent(self, event):  # todo rework this shit
        self.oldPos = event.globalPosition().toPoint()

    def mouseMoveEvent(self, event):  # todo rework this shit
        delta = QPoint(event.globalPosition().toPoint() - self.oldPos)
        self.move(self.x() + delta.x(), self.y() + delta.y())
        self.oldPos = event.globalPosition().toPoint()


class MyWeather(QWidget):

    def __init__(self):
        super().__init__()

        self.wether5days = None

        self.label = QLabel()
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label.setWordWrap(True)

        layout = QHBoxLayout()
        layout.addWidget(self.label)

        self.setLayout(layout)

        self.get_weather_string()

    def mousePressEvent(self, event):
        self.wether5days = WeatherForDaysWidget(self.get_weather_string_5_days)
        self.wether5days.show()

    def get_weather_string_5_days(self) -> str:

        rezult = ''

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
            res = requests.get("http://api.openweathermap.org/data/2.5/forecast",
                               params={'id': city_id, 'units': 'metric', 'lang': 'ru', 'APPID': appid})
            data = res.json()
            for i in data['list']:
                # print(i['dt_txt'], '{0:+3.0f}'.format(i['main']['temp']), i['weather'][0]['description'])
                rezult += (i['dt_txt'] + '\t' + '{0:+3.0f}'.format(i['main']['temp']) + '\t' + i['weather'][0][
                    'description']) + '\n'

        except Exception as e:
            print("Exception (forecast):", e)
            pass
        return rezult

    def get_weather_string(self):
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
            self.label.setText(
                '{}\n {}\n {}{}'.format('Анапа:', data['weather'][0]['description'], data['main']['temp'], '°'))
        else:
            # return 'ᓚᘏᗢ'
            self.label.setText('ᓚᘏᗢ')


def print_to_string(*args, **kwargs):
    output = io.StringIO()
    print(*args, file=output, **kwargs)
    contents = output.getvalue()
    output.close()
    return contents
