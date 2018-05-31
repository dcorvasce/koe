class DB(object):
    '''Provides methods to execute common operations on a database'''
    def __init__(self, connection, cursor):
        self.connection = connection
        self.cursor = cursor
    
    def selectAll(self, query, parameters):
        '''Executes a selection and returns all the matches'''
        self.cursor.execute(query, parameters)
        return self.cursor.fetchall()
    
    def insert(self, table, columns):
        '''Executes an insert and returns the inserted rows'''
        column_names = ','.join([column for column in columns])
        placeholders = ['%s'] * len(columns)

        query = 'INSERT INTO %s (%s) VALUES(%s)' % (table, column_names, ','.join(placeholders))

        self.cursor.execute(query, tuple([columns[index] for index in columns]))
        self.connection.commit()

        return self.cursor.lastrowid or None