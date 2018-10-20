# -*- coding: utf-8 -*-
import logging

import mysql.connector

from .abstractdb import AbstractDB


class MysqlDB(AbstractDB):

    def __init__(self, ip="127.0.0.1", port=27017, dbname="pastepwn", username=None, password=None):
        super().__init__()
        self.logger = logging.getLogger(__name__)
        self.logger.debug("Initializing MySQLDB - {0}:{1}".format(ip, port))

        self.db = mysql.connector.connect(
            host=ip,
            user=username,
            passwd=password,
            database=dbname
        )

        self.cursor = self.db.cursor()
        self._create_tables()

        self.logger.debug("Connected to database!")

    def _create_tables(self):
        self.cursor.execute("""CREATE TABLE 'pastes' (
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
