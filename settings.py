import sqlite3

class Settings:
    def __init__(self):
        self.base = sqlite3.connect("setup.db")
        self.cursor = self.base.cursor()
    
    def load_settings(self, value):
        return self.cursor.execute("""SELECT Value FROM settings WHERE Name = '{0}'""".format(value)).fetchall()[0][0]