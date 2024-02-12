#####################################
#            Created by             #
#                SBR                #
#####################################
import copy
import json
import os
import sqlite3
#####################################


class DB:
    def __init__(self, path):
        super(DB, self).__init__()
        self.__db_path = path
        self.cursor = None
        self.db = None
        self.init()

    def init(self):
        if not os.path.exists(self.__db_path):
            self.db = sqlite3.connect(self.__db_path, check_same_thread=False)
            self.cursor = self.db.cursor()
            self.cursor.execute('''CREATE TABLE users(
            name text,
            year text,
            janre text,
            rate text,
            country text,
            watchtime text,
            desc text,
            link text,
            cover BLOB,
            UNIQUE(name, year, janre, rate, country, watchtime, desc, link, cover)
            )
            ''')
            self.db.commit()
        else:
            self.db = sqlite3.connect(self.__db_path, check_same_thread=False)
            self.cursor = self.db.cursor()

    def db_write(self, data):
        self.cursor.execute('INSERT OR IGNORE INTO films VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)', (data[0], data[1], data[2], data[3], data[4], data[5], data[6], data[7], data[8]))
        self.db.commit()

    def db_read(self, data, mode):
        out = []
        years = []
        if mode == 'year' and '-' in data:
            years.extend(data.split('-'))
            self.cursor.execute(f'SELECT name, year, janre, rate, country, watchtime, desc, link, cover FROM films WHERE {mode} BETWEEN {years[0]} AND {years[1]} order by name')
        else:
            self.cursor.execute(f'SELECT name, year, janre, rate, country, watchtime, desc, link, cover FROM films WHERE {mode} LIKE "%{data}%" order by name')
        self.db.commit()
        for i in self.cursor.fetchall():
            out.append(i)
        if len(out) != 0:
            return out