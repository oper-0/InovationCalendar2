from PyQt6.QtCore import QPoint
from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import QLabel


class MyFooterImage(QLabel):
    def __init__(self, moover, parent_x, parent_y):
        super().__init__()

        self.parentMover = moover
        self.parentX = parent_x
        self.parentY = parent_y

        pixmap = QPixmap(r'assets/bg_ver_3.png')
        self.setPixmap(pixmap)

    def mousePressEvent(self, event): # todo rework this shit
        self.oldPos = event.globalPosition().toPoint()

    def mouseMoveEvent(self, event): # todo rework this shit
        delta = QPoint(event.globalPosition().toPoint() - self.oldPos)
        self.parentMover(self.parentX() + delta.x(), self.parentY() + delta.y())
        self.oldPos = event.globalPosition().toPoint()