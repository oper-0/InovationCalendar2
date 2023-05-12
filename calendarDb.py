import sqlite3
import holidays

class calendarDB:

    def __init__(self, path):
        self.con = sqlite3.connect(path)
        self.cur = self.con.cursor()


    def _generate_data(self):
        ...



