# nfatools form3 db

import mysql.connector
import traceback

import logging
logger = logging.getLogger(__name__)

class Database():

    def __init__(self, host, port, username, password, database):
        self.connection = None
        self.host = host
        self.port = port
        self.username = username
        self.password = password
        self.database = database

        # connect without specifying a database
        if not self.connect(database=None):
            raise RuntimeError(f"Failed connection to database {self.connection_string()}")

        # verify the expected database is present
        with Cursor(self.connection) as cursor:
            rows = cursor.query('show databases;')
            available_databases = [r[0] for r in rows]
        logger.debug(f"databases found: {repr(available_databases)}")

        if not self.database in available_databases:
            raise RuntimeError(f"Database {self.database} is not present.")

        # specify the database we need
        with Cursor(self.connection) as cursor:
            cursor.execute(f'use {self.database};')

        # detect database with no tables
        with Cursor(self.connection) as cursor:
            tables = cursor.query('show tables;')
        if not tables:
            raise RuntimeError('Database has no tables')

    def __enter__(self):
        return self

    def __exit__(self, etype, value, tb):
        self.close()

    def __del__(self):
        self.close()

    def close(self):
        if self.connection:
            self.connection.close()
            self.connection = None

    def __str__(self):
        """return string representaton for this instance"""
        return f'Database<{hex(id(self))}>'

    def __repr__(self):
        """return a string with server connection details"""
        return f"{self} {self.connection_string()}"

    def cursor(self, **kwargs):
        """return a Cursor configured with the database connection"""
        return Cursor(self.connection, **kwargs)

    def dict_cursor(self, **kwargs):
        kwargs['dictionary']=True
        return self.cursor(self.connection, **kwargs)

    def connection_string(self):
        return f"'{self.database}' on '{self.user}@{self.host}'"

    def connect(self, database=None):
        try:
            self.connection = mysql.connector.connect(host=self.host, user=self.username, password=self.password, database=database)
            self.connection.get_warnings = True
        except mysql.connector.Error as e:
            return self.inactive_server_error(e)
        else:
            return self.connection


"""
The Cursor() class wraps the mysql.connector.connection.cursor() class in a
context manager.  It supports execute() and query() functions, with local
exception handling passing diagnostic and debugging data to the logging 
system on errors.

Example: 

    with Cursor(cxn) as cursor:
        rows = cursor.execute('show databases;')

    for row in rows:
        print(repr(row))
    
"""

class Cursor():
    """
    A context managed database cursor for mysql.connector cursors.
    """

    def __init__(self, cxn, **kwargs):
        """
        Cursor() Constructor

        :param cxn: the mysql.connector.connection instance use for creating the cursor
        :param **kwargs: keyword arguments (see below)
        :return: returns nothing
        
        The following keyword arguments may be passed boolean values:

        commit - call commit() before closing the connection
        ignore_warnings - query() function will request and log MySQL warnings
        ignore_notes - query() function will ignore 'Note' type warnings
        dictionary - query() will return rows as type dict()
        buffered - passed to the cursor() constructor to modify its function (see MySQL documentation)
        """

        self.cxn = cxn
        self.sql = ''
        self.lastrowid = -1
        self.ignore_warnings = kwargs.get('ignore_warnings', False)
        self.ignore_notes = kwargs.get('ignore_notes', True)
        self.commit = kwargs.get('commit', False)
        self.cursor = cxn.cursor(dictionary=kwargs.get('dictionary', False), buffered=kwargs.get('buffered', False))

    def __str__(self):
        return f"Cursor<{hex(id(self))}>"

    def __repr__(self):
        return self.__str__()

    def __enter__(self):
        return self

    def __exit__(self, etype, value, tb):
        if self.commit:
            self.cxn.commit()
        self.cursor.close()

    def execute(self, *args, **kwargs):
        sql = repr(args)
        try:
            result = self.cursor.execute(*args, **kwargs)
            assert result == None
            self.lastrowid = self.cursor.lastrowid
        except mysql.connector.Error as e:
            f = traceback.extract_stack()[-3]
            logger.debug(f"{repr(self)}\n SQL Error {e}\n  caller={f.filename}:{f.lineno}\n  query={sql}")
            logger.error(f"{self} Query Failed with Error {e}")
            raise e
        return self.cursor

    def query(self, *args, **kwargs):
        self.sql = args
        rows = self.execute(*args, **kwargs).fetchall()

        if not self.ignore_warnings:
            self.handle_warnings()

        return rows

    def handle_warnings(self):
        for warning in self.cursor.fetchwarnings() or []:
            if warning[0] == 'Note' and self.ignore_notes:
                pass
            else:
                logger.warning(f"{repr(self)} SQL Warning: {warning}")
