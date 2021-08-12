# -*- coding: utf-8 -*-
import logging
import pathlib
import sqlite3

from .abstractdb import AbstractDB


class SQLiteDB(AbstractDB):
    """Database class representing an sqlite database instance"""

    def __init__(self, dbpath="pastepwn"):
        super().__init__()
        self.dbpath = pathlib.Path(dbpath)
        self.logger = logging.getLogger(__name__)
        self.logger.debug("Initializing SQLite - {0}".format(self.dbpath))

        # Check if the folder path exists
        if not self.dbpath.exists():
            # If not, create the path and the file
            dbdir = self.dbpath.parent
            if not dbdir.exists():
                dbdir.mkdir()
            self.dbpath.touch()
        elif self.dbpath.is_dir():
            raise ValueError("'{0}' is a directory. Use different path/name for database.".format(self.dbpath))

        try:
            self.db = sqlite3.connect(str(self.dbpath), check_same_thread=False)
        except Exception as e:
            self.logger.exception("An exception happened when initializing the database: {0}".format(e))
            raise

        self.db.text_factory = lambda x: str(x, "utf-8", "ignore")
        self.cursor = self.db.cursor()
        self._create_tables()

        self.logger.debug("Connected to database!")

    def _create_tables(self):
        self.dbpath.touch()

        self.cursor.execute("""CREATE TABLE IF NOT EXISTS 'pastes' (
                            'key'	TEXT NOT NULL UNIQUE,
                            'title'	TEXT,
                            'user'	TEXT,
                            'size'	INTEGER,
                            'date'	INTEGER,
                            'expire'	INTEGER,
                            'syntax'	TEXT,
                            'scrape_url'	TEXT,
                            'full_url'	TEXT,
                            'body'	TEXT,
                            PRIMARY KEY('key'))""")
        self.db.commit()

    def _insert_data(self, paste):
        self.cursor.execute("INSERT INTO pastes (key, title, user, size, date, expire, syntax, scrape_url, full_url, body) "
                            "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                            (paste.key, paste.title, paste.user, paste.size, paste.date, paste.expire, paste.syntax,
                             paste.scrape_url, paste.full_url, paste.body
                             )
                            )
        self.db.commit()

    def _update_data(self, paste):
        self.cursor.execute("UPDATE pastes SET body = ? WHERE key = ?", (paste.body, paste.key))
        self.db.commit()

    def _get_data(self, key, value):
        pass

    def close_connection(self):
        """Closes the connection to the sqlite database"""
        self.cursor.close()
        self.db.close()

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
            if "UNIQUE constraint failed: pastes.key" in str(e):
                self.logger.debug("Doing upsert")
                self._update_data(paste)

    def get(self, key):
        return self._get_data("key", key)
