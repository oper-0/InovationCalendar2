# importing required librarie
import sys

from PyQt6 import QtCore, QtGui
from PyQt6.QtCore import QPoint, QTimer
from PyQt6.QtGui import QIcon, QPalette, QBrush, QColor, QLinearGradient
from PyQt6.QtWidgets import QVBoxLayout, QWidget, QApplication, QHBoxLayout

# from InnovationCalendar import InnovationCalendar
# from clock import MyClock
import PyQt6

from qt_material import apply_stylesheet

from calendarWidget import InnovationCalendar
from clockWidget import MyClock
from footerImage import MyFooterImage
from weatherWidget import MyWeather


class Window(QWidget):

    def __init__(self):
        super().__init__()

        self.setWindowFlags(QtCore.Qt.WindowType.FramelessWindowHint)

        self.setWindowIcon(QIcon('era_star.png'))
        self.setWindowTitle("Цифровой календарь")
        self.setStyleSheet("background-image: url(bg_all_2.jpg); background-attachment: scroll")


        w = 380
        h = 500
        self.setFixedSize(w, h)

        layout = QVBoxLayout()
        header = QHBoxLayout()

        calendar = InnovationCalendar()

        clock = MyClock()

        self.weather = MyWeather()

        header.addWidget(clock)
        header.addWidget(self.weather)

        layout.addLayout(header)
        layout.addWidget(calendar)

        layout.addWidget(MyFooterImage(self.move, self.x, self.y))

        self.setLayout(layout)

    # def mousePressEvent(self, event): # todo rework this shit
    #     self.oldPos = event.globalPosition().toPoint()
    #
    # def mouseMoveEvent(self, event): # todo rework this shit
    #     delta = QPoint(event.globalPosition().toPoint() - self.oldPos)
    #     self.move(self.x() + delta.x(), self.y() + delta.y())
    #     self.oldPos = event.globalPosition().toPoint()


App = QApplication(sys.argv)
window = Window()

timer = QTimer()
timer.timeout.connect(window.weather.get_weather_string)  # execute `display_time`
timer.setInterval(1000000)  # 16.6 min
timer.start()

# apply_stylesheet(App, theme='dark_amber.xml')
apply_stylesheet(App, theme='dark_blue.xml')
# apply_stylesheet(App, theme='dark_cyan.xml')
# apply_stylesheet(App, theme='dark_lightgreen.xml')
# apply_stylesheet(App, theme='dark_medical.xml')
# apply_stylesheet(App, theme='dark_pink.xml')
# apply_stylesheet(App, theme='dark_purple.xml')
# apply_stylesheet(App, theme='dark_red.xml')
# apply_stylesheet(App, theme='dark_teal.xml')
# apply_stylesheet(App, theme='dark_yellow.xml')
# apply_stylesheet(App, theme='light_amber.xml')
# apply_stylesheet(App, theme='light_blue.xml')
# apply_stylesheet(App, theme='light_blue_500.xml')
# apply_stylesheet(App, theme='light_cyan.xml')
# apply_stylesheet(App, theme='light_cyan_500.xml')

window.show()
App.exec()
