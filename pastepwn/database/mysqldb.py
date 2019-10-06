# -*- coding: utf-8 -*-
import logging

import mysql.connector

from .abstractdb import AbstractDB


class MysqlDB(AbstractDB):

    def __init__(self, ip="127.0.0.1", port=3306, unix_socket=None, dbname="pastepwn", username=None, password=None, timeout=10):
        super().__init__()
        self.logger = logging.getLogger(__name__)
        self.logger.debug("Initializing MySQLDB - {0}:{1}".format(ip, port))

        # https://dev.mysql.com/doc/connector-python/en/connector-python-connectargs.html
        if unix_socket:
            self.db = mysql.connector.connect(
                host=ip,
                user=username,
                passwd=password,
                unix_socket=unix_socket,
                connection_timeout=timeout
            )
        else:
            self.db = mysql.connector.connect(
                host=ip,
                port=port,
                user=username,
                passwd=password,
                database=dbname,
                connection_timeout=timeout
            )

        self.cursor = self.db.cursor()
        # self._create_db(dbname) # Not used because of possible SQLI
        self._create_tables()

        self.logger.debug("Connected to database!")

    def _create_db(self, dbname):
        # Currently I found no other way to insert the database name into the sql statement
        # With the following code a simple SQL Injection would be possible - question is, why would a user do this to his own database?
        # Nevertheless I don't want to put this into production that way. I'll keep the code but remove the call to it.
        self.logger.info("Creating database '{0}' (if not exists)".format(self.dbname))
        self.cursor.execute("""CREATE DATABASE IF NOT EXISTS %s;""" % self.dbname)
        self.cursor.execute("""USE %s;""" % self.dbname)
        self.db.commit()

    def _create_tables(self):
        # Although the length of 'key' should never exceed 8 chars,
        # making it longer prevents from future issues.
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS `pastes` (
                                    `key` VARCHAR(30) NOT NULL UNIQUE,
                                    `title` TEXT,
                                    `user` TEXT,
                                    `size` INTEGER,
                                    `date` INTEGER,
                                    `expire` INTEGER,
                                    `syntax` TEXT,
                                    `scrape_url` TEXT,
                                    `full_url` TEXT,
                                    `body` TEXT,
                                    PRIMARY KEY(`key`));""")
        self.db.commit()

    def _insert_data(self, paste):
        self.cursor.execute("INSERT INTO `pastes` (`key`, `title`, `user`, `size`, `date`, `expire`, `syntax`, `scrape_url`, `full_url`, `body`) "
                            "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s);",
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
        raise NotImplementedError

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
