from typing import Callable

from PyQt6 import QtCore
from PyQt6.QtCore import QDate, Qt, QPoint
from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QMessageBox, QWidget, QVBoxLayout, QLabel, QHBoxLayout, QLineEdit, QPushButton, QDialog, \
    QDialogButtonBox, QPlainTextEdit, QFrame


class MyDialog(QDialog):
    def __init__(self, date: QDate, savingFun: Callable[[str, QDate], None]):
        super().__init__()
        self.setWindowFlags(QtCore.Qt.WindowType.FramelessWindowHint)
        self.savingFun = savingFun

        self.date = date

        self.setWindowIcon(QIcon(r'assets/era_star_24.png'))
        layout = QVBoxLayout()

        date_label = QLabel(date.toString("dd.MM.yyyy"))
        date_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # msg_input = QLineEdit()
        self.msg_input = QPlainTextEdit()
        self.msg_input.setPlaceholderText('Введите заметку')

        footer = QHBoxLayout()

        self.submit_btn = QPushButton('OК')
        self.submit_btn.clicked.connect(self.btn_accept)
        cancel_btn = QPushButton('ОТМЕНА')
        cancel_btn.clicked.connect(self.btn_reject)
        footer.addWidget(self.submit_btn)
        footer.addWidget(cancel_btn)

        layout.addWidget(date_label)
        layout.addWidget(self.msg_input)

        layout.addLayout(footer)


        self.setLayout(layout)
        # self.set

    def btn_accept(self):
        self.savingFun(self.msg_input.toPlainText(), self.date)
        self.close()

    def btn_reject(self):
        self.close()

    def mousePressEvent(self, event):  # todo rework this shit
        self.oldPos = event.globalPosition().toPoint()

    def mouseMoveEvent(self, event):  # todo rework this shit
        delta = QPoint(event.globalPosition().toPoint() - self.oldPos)
        self.move(self.x() + delta.x(), self.y() + delta.y())
        self.oldPos = event.globalPosition().toPoint()
