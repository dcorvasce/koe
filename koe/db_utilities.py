from pymysql import cursors
from config.database import create_connection

'''Provide a class to interact with the database'''
class DB(object):
    '''Provide methods to execute common operations on a database'''
    def __init__(self):
        self.connection = create_connection()
        self.cursor = self.connection.cursor(cursors.DictCursor)


    def _refresh_cursor(self):
        self.cursor.close()
        self.cursor = self.connection.cursor(cursors.DictCursor)


    def select_all(self, query, parameters):
        '''Execute a selection and return all the matches'''
        self._refresh_cursor()
        self.cursor.execute(query, parameters)
        self.connection.commit()
        return self.cursor.fetchall()


    def query(self, query, parameters):
        '''Execute a general query which return rows'''
        self._refresh_cursor()
        self.cursor.execute(query, parameters)
        self.connection.commit()
        return self.cursor


    def insert(self, table, columns):
        '''Execute an insert and return the inserted rows'''
        column_names = ','.join([column for column in columns])
        placeholders = ['%s'] * len(columns)

        self._refresh_cursor()
        self.cursor.execute('SET NAMES utf8mb4')
        self.connection.commit()

        query = 'INSERT INTO %s (%s) VALUES(%s)' % (table, column_names, ','.join(placeholders))

        self.cursor.execute(query, tuple([columns[index] for index in columns]))
        self.connection.commit()

        return self.cursor.lastrowid or None
