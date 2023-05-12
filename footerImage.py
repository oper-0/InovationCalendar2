from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import QLabel


class MyFooterImage(QLabel):
    def __init__(self):
        super().__init__()
        pixmap = QPixmap(r'assets/bg_ver_3.png')
        self.setPixmap(pixmap)
