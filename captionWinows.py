import sys
from typing import Callable

from PyQt6 import QtCore
from PyQt6.QtCore import QDate, Qt, QPoint
from PyQt6.QtGui import QIcon, QAction
from PyQt6.QtWidgets import QMessageBox, QWidget, QVBoxLayout, QLabel, QHBoxLayout, QLineEdit, QPushButton, QDialog, \
    QDialogButtonBox, QPlainTextEdit, QApplication, QFrame, QGraphicsBlurEffect

from utilits import DateDataFields, DateType


class captionListItem(QWidget):

    def __init__(self, record: dict, deletingFunc: Callable[[dict], None]):
        super().__init__()

        self.record = record
        self.deletingFunc = deletingFunc

        title = record.get(DateDataFields.date).toString("MM.dd.yyyy")
        caption = record.get(DateDataFields.message)

        header = QHBoxLayout()

        title = QLabel(title)
        title.setAlignment(Qt.AlignmentFlag.AlignLeft)

        header.addWidget(title, stretch=4)

        self.delete_button = QPushButton('')
        self.delete_button.setIcon(QIcon(r'assets\trash_24.png'))
        # if record.get(DateDataFields.type == DateType.MESSAGE):
        header.addWidget(self.delete_button, stretch=1)
        self.delete_button.clicked.connect(self.delet_record)

        # delete_widget = QWidget()
        # delete_action = QAction(QIcon(r'assets\trash_24.png'), "удалить запись", delete_widget)
        # delete_action.triggered.connect(self.delete_record_func)
        # delete_widget.addAction(delete_action)
        # header.addWidget(delete_widget)

        caption = QLabel(caption)
        caption.setWordWrap(True)

        layout = QVBoxLayout()
        layout.addLayout(header)
        layout.addWidget(caption)

        self.mainFrame = QFrame()
        self.mainFrame.setLayout(layout)
        # mainFrame.setStyleSheet('QFrame {border:1px solid rgb(0, 255, 0);}')

        mainLayout = QVBoxLayout()
        mainLayout.addWidget(self.mainFrame)

        # self.setLayout(layout)
        self.setLayout(mainLayout)

    def delet_record(self):
        self.deletingFunc(self.record)
        self.mainFrame.setGraphicsEffect(QGraphicsBlurEffect())


class captionList(QWidget):
    def __init__(self, records: list[dict], deleteingFunc: Callable[[dict], None]):
        super().__init__()
        self.setWindowFlags(QtCore.Qt.WindowType.FramelessWindowHint)
        self.resize(300, 100)

        title = QLabel('ЗАПИСИ:')
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)

        layout = QVBoxLayout()

        layout.addWidget(title)

        for r in records:
            layout.addWidget(captionListItem(r, deleteingFunc))  # todo type?

        # layout.addWidget(captionListItem('2023-04-15', 'yare yare yare yare yare yare yare yare yare yare yare yare v'))
        # layout.addWidget(captionListItem('2023-04-15', 'yare yare yare yare yare yare yare yare yare yare yare yare v'))
        # layout.addWidget(captionListItem('2023-04-15', 'yare yare yare yare yare yare yare yare yare yare yare yare v'))
        # layout.addWidget(captionListItem('2023-04-15', 'yare yare yare yare yare yare yare yare yare yare yare yare v'))

        self.setLayout(layout)


    def mousePressEvent(self, event):  # todo rework this shit
        self.oldPos = event.globalPosition().toPoint()

    def mouseMoveEvent(self, event):  # todo rework this shit
        delta = QPoint(event.globalPosition().toPoint() - self.oldPos)
        self.move(self.x() + delta.x(), self.y() + delta.y())
        self.oldPos = event.globalPosition().toPoint()

    # A key has been pressed!
    def keyPressEvent(self, event):
        # Did the user press the Escape key?
        if event.key() == Qt.Key.Key_Escape:  # QtCore.Qt.Key_Escape is a value that equates to what the operating system passes to python from the keyboard when the escape key is pressed.
            # Yes: Close the window
            self.close()
        # No:  Do nothing.