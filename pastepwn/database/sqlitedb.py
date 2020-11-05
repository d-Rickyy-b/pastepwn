# -*- coding: utf-8 -*-
import logging
import os
import sqlite3

from .abstractdb import AbstractDB


class SQLiteDB(AbstractDB):

    def __init__(self, dbpath="pastepwn"):
        """
        Initialize the database.

        Args:
            self: (todo): write your description
            dbpath: (str): write your description
        """
        super().__init__()
        self.dbpath = dbpath
        self.logger = logging.getLogger(__name__)
        self.logger.debug("Initializing SQLite - {0}".format(dbpath))

        # Check if the folder path exists
        if not os.path.exists(dbpath):
            # If not, create the path and the file
            dbdir = os.path.dirname(dbpath)
            if dbdir != '':
                os.mkdir(dbdir)
            open(self.dbpath, "a").close()
        elif os.path.isdir(dbpath):
            raise ValueError('\'{0}\' is a directory. Use different path/name for database.'.format(dbpath))

        try:
            self.db = sqlite3.connect(dbpath, check_same_thread=False)
            self.db.text_factory = lambda x: str(x, 'utf-8', "ignore")
            self.cursor = self.db.cursor()
            self._create_tables()
        except Exception as e:
            self.logger.exception("An exception happened when initializing the database: {0}".format(e))
            raise

        self.logger.debug("Connected to database!")

    def _create_tables(self):
        """
        Create all tables. tables in the database.

        Args:
            self: (todo): write your description
        """
        open(self.dbpath, "a").close()

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
        """
        Inserts data to the database.

        Args:
            self: (todo): write your description
            paste: (todo): write your description
        """
        self.cursor.execute("INSERT INTO pastes (key, title, user, size, date, expire, syntax, scrape_url, full_url, body) "
                            "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
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

    def _update_data(self, paste):
        """
        Updates data from db

        Args:
            self: (todo): write your description
            paste: (todo): write your description
        """
        self.cursor.execute("UPDATE pastes SET body = ? WHERE key = ?",
                            (paste.body,
                            paste.key))
        self.db.commit()

    def _get_data(self, key, value):
        """
        Gets the value of a key.

        Args:
            self: (todo): write your description
            key: (str): write your description
            value: (todo): write your description
        """
        pass

    def count(self, key, value):
        """
        Return the number of values in the set stored at key.

        Args:
            self: (todo): write your description
            key: (str): write your description
            value: (todo): write your description
        """
        # TODO add filter to counting
        return self.cursor.execute("SELECT count(*) FROM pastes")

    def count_all(self):
        """
        Counts all the number of results

        Args:
            self: (todo): write your description
        """
        return self.cursor.execute("SELECT count(*) FROM pastes")

    def store(self, paste):
        """
        Stores data into the clipboard

        Args:
            self: (todo): write your description
            paste: (todo): write your description
        """
        self.logger.debug("Storing paste {0}".format(paste.key))

        try:
            self._insert_data(paste)
        except Exception as e:
            self.logger.debug("Exception '{0}'".format(e))
            if "UNIQUE constraint failed: pastes.key" in str(e):
                self.logger.debug("Doing upsert")
                self._update_data(paste)

    def get(self, key):
        """
        Returns the value of the key.

        Args:
            self: (todo): write your description
            key: (todo): write your description
        """
        return self._get_data("key", key)
