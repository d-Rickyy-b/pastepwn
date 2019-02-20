# -*- coding: utf-8 -*-
import logging
import os
import sqlite3

from .abstractdb import AbstractDB


class SQLiteDB(AbstractDB):

    def __init__(self, dbpath="pastepwn"):
        super().__init__()
        self.dbpath = dbpath
        self.logger = logging.getLogger(__name__)
        self.logger.debug("Initializing SQLite - {0}".format(dbpath))

        # Check if the folder path exists
        if not os.path.exists(os.path.dirname(dbpath)):
            # If not, create the path and the file
            os.mkdir(os.path.dirname(dbpath))
            open(self.dbpath, "a").close()

        try:
            self.db = sqlite3.connect(dbpath)
            self.db.text_factory = lambda x: str(x, 'utf-8', "ignore")
            self.cursor = self.db.cursor()
            self._create_tables()
        except Exception as e:
            self.logger.exception("An exception happened when initializing the database: {0}".format(e))
            raise

        self.logger.debug("Connected to database!")

    def _create_tables(self):
        open(self.dbpath, "a").close()

        self.cursor.execute("""CREATE TABLE IF NOT EXISTS 'pastes' (
                            'key'	TEXT NOT NULL UNIQUE,
                            'title'	TEXT,
                            'user'	TEXT,
                            'size'	INTEGER,
                            'date'	INTEGER,
                            'expire'	INTEGER,
                            'scrape_url'	TEXT,
                            'full_url'	TEXT,
                            'body'	TEXT,
                            PRIMARY KEY('key'))""")
        self.db.commit()

    def _insert_data(self, paste):
        self.cursor.execute("INSERT INTO pastes (key, title, user, size, date, expire, syntax, scrape_url, full_url, body) "
                            "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
                            (paste.key,
                             paste.title,
                             paste.user,
                             paste.size,
                             paste.date,
                             paste.expire,
                             paste.syntax,
                             paste.scrape_url,
                             paste.full_url,
                             paste.body))
        self.db.commit()

    def _get_data(self, key, value):
        pass

    def count(self, key, value):
        # TODO add filter to counting
        return self.cursor.execute("SELECT count(*) FROM pastes")

    def count_all(self):
        return self.cursor.execute("SELECT count(*) FROM pastes")

    def store(self, paste):
        self.logger.debug("Storing paste {0}".format(paste.key))

        try:
            self._insert_data(paste)
        except Exception as e:
            self.logger.debug("Exception '{0}'".format(e))

    def get(self, key):
        return self._get_data("key", key)
