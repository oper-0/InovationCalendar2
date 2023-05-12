# importing required librarie
import sys
from PyQt6.QtWidgets import QApplication, QWidget
from PyQt6.QtWidgets import QVBoxLayout, QLabel
from PyQt6.QtGui import QFont
from PyQt6.QtCore import QTimer, QTime, Qt


class MyClock(QWidget):

    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        font = QFont('Courier New', 120)
        self.label = QLabel()
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label.setFont(font)
        self.label.setStyleSheet('font-size: 32px;')
        layout.addWidget(self.label)
        self.setLayout(layout)
        timer = QTimer(self)
        timer.timeout.connect(self.showTime)
        timer.start(1000)

        self.setStyleSheet("background-image: url(assets\\bg_all_2.jpg); background-attachment: fixed")

    def showTime(self):
        current_time = QTime.currentTime()
        label_time = current_time.toString('hh:mm:ss')
        self.label.setText(label_time)
