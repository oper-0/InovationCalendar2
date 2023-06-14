import enum

import PyQt6
from PyQt6.QtCore import QDate, Qt, QPoint
from PyQt6.QtGui import QImage, QAction, QPainter, QFont
from PyQt6.QtWidgets import QCalendarWidget, QMenu, QComboBox, QWidgetAction
import pickle

from captionWinows import captionList
from dialogWidget_setMessage import MyDialog
from utilits import DateType, DateDataFields


class InnovationCalendar(QCalendarWidget):

    def __init__(self):
        super().__init__()

        self.captionList = None
        self.add_holiday = None
        self.add_message = None
        self.addToCalendarWindow: MyDialog = None

        self.dates_data = []

        self.dataPath: str = r'datesData.pickle'
        # self.marks = self.load_marks()
        # self.holidays = self.load_holidays()

        # self._generate_dates_data() # todo delete me

        # self.build_context_menu()

        # self.setGraphicsEffect(PyQt6.QtWidgets.QGraphicsColorizeEffect())

        self.clicked.connect(self.lkm_click)
        # self.activated.connect(self.pkm_click)

        self.create_actions()

        self.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.customContextMenuRequested.connect(self.context_menu)

        self.update_dates_data()

    # def build_context_menu(self):
    #     self.context_menu = QMenu(self)
    #     add_event = self.context_menu.addAction("Добавить запись")

    def create_actions(self):
        self.add_message = QAction('Заметку')
        self.add_message.triggered.connect(self.add_message_func)
        self.add_holiday = QAction('Событие')
        self.add_holiday.triggered.connect(self.add_holiday_func)

    def add_message_func(self):
        self.addToCalendarWindow = MyDialog(self.selectedDate(), self.save_message)
        self.addToCalendarWindow.show()

    def save_message(self, text: str, date: QDate):
        print(date, text)
        self.add_dates_data(date, text, DateType.MESSAGE)

    def add_holiday_func(self):
        print('add_hld')

    def context_menu(self, pos):
        m = QMenu(self)
        sub = QMenu(m)
        sub.setTitle('Добавить')

        sub.addAction(self.add_message)
        sub.addAction(self.add_holiday)
        m.addMenu(sub)

        pos = self.mapToGlobal(pos)
        m.move(pos)
        m.show()

    def paintCell(self, painter, rect, date):
        QCalendarWidget.paintCell(self, painter, rect, date)

        s = 2

        if date.dayOfWeek()>5:
            painter.setPen(Qt.GlobalColor.gray)
            painter.drawRect(rect.x()+s, rect.y()+s, rect.width()-2*s, rect.height()-2*s)

        if self.is_exist(DateDataFields.type, DateType.MESSAGE, date):
            # painter.drawImage(rect.x(), rect.y(), QImage(r'assets\molecule24.png'))
            painter.drawImage(rect.x(), rect.y(), QImage(r'assets\era_star_24.png'))

        if self.is_exist(DateDataFields.type, DateType.HOLIDAY, date):
            painter.drawImage(rect.x(), rect.y(), QImage(r'assets\confetti_24.png'))
            painter.setPen(Qt.GlobalColor.gray)
            painter.drawRect(rect.x()+s, rect.y()+s, rect.width()-2*s, rect.height()-2*s)
            # painter.drawEllipse(rect.x() + s, rect.y() + s, rect.width() - 2 * s, rect.height() - 2 * s)

    def is_exist(self, key, val, date):
        for i in self.dates_data:
            if i.get(key) != val:
                continue
            if i.get(DateDataFields.date) != date:
                continue
            return i

    def lkm_click(self):
        date = self.selectedDate()
        dates = [d[DateDataFields.date] for d in self.dates_data if DateDataFields.date in d]
        if date in dates:
            self.show_captions(date, dates)

        # self.show_msg(date)

    def pkm_click(self, event):
        self.context_menu.exec(event.globalPos())

    # def contextMenuEvent(self, event):
    #     # Show the context menu
    #     self.context_menu.exec(event.globalPos())

    def generate_holidays(self):
        pass

    def update_dates_data(self):
        self.dates_data.clear()
        with open(self.dataPath, "rb") as infile:
            self.dates_data = pickle.load(infile)

    def add_dates_data(self, date: QDate, txt: str, type: DateType):
        self.update_dates_data()
        self.dates_data.append({DateDataFields.date: date,
                                DateDataFields.message: txt,
                                DateDataFields.type: type})
        with open(self.dataPath, "wb") as outfile:
            pickle.dump(self.dates_data, outfile)

    def delete_dates_data(self, pop_record: dict[QDate, str, DateType]):
        if pop_record not in self.dates_data:
            return
        self.dates_data.pop(self.dates_data.index(pop_record))
        with open(self.dataPath, "wb") as outfile:
            pickle.dump(self.dates_data, outfile)
        print('dates data length now is: {}'.format(len(self.dates_data)))


    def _generate_dates_data(self):
        dates_data = [
            {DateDataFields.date: QDate(2023, 5, 9), DateDataFields.message: 'День победы',
             DateDataFields.type: DateType.HOLIDAY},
            {DateDataFields.date: QDate(2023, 5, 14), DateDataFields.message: 'День рождения ряд. Иванова',
             DateDataFields.type: DateType.MESSAGE},
            {DateDataFields.date: QDate(2023, 5, 23), DateDataFields.message: 'Наряд',
             DateDataFields.type: DateType.MESSAGE},
            {DateDataFields.date: QDate(2023, 5, 5), DateDataFields.message: 'Строевой смотр',
             DateDataFields.type: DateType.MESSAGE},
            {DateDataFields.date: QDate(2023, 5, 5), DateDataFields.message: 'Концерт в 18:00',
             DateDataFields.type: DateType.MESSAGE},
            {DateDataFields.date: QDate(2023, 5, 1), DateDataFields.message: 'Праздник 1 мая',
             DateDataFields.type: DateType.HOLIDAY},
            {DateDataFields.date: QDate(2023, 5, 8), DateDataFields.message: 'День победы',
             DateDataFields.type: DateType.HOLIDAY},
        ]
        with open(self.dataPath, "wb") as outfile:
            pickle.dump(dates_data, outfile)

    def show_captions(self, date: QDate, dates: list[QDate]):
        idxs = [i for i in range(len(dates)) if dates[i] == date]
        req_records = [self.dates_data[idx] for idx in idxs]

        if not req_records:
            return

        self.captionList = captionList(req_records, self.delete_dates_data)
        self.captionList.show()
