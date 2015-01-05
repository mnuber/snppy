import sqlite3

##SQLAdapter is an class with functions to easily access a SQLite3 database

class SQLAdapter(object):
    
    table = ""
    columns = tuple()
    
    def __init__(self, filename):
        self.conn = sqlite3.connect(filename)
        self.conn.text_factory = str 
        self.cursor = self.conn.cursor()    

    def set_table(self, table):
        self.table = table

    def get_table(self):
        return self.table

    def select_all(self):
        return self.cursor.execute("SELECT * FROM " + self.get_table())

    def select_row(self, column, cid):
        self.cursor.execute("SELECT " + '*' + " FROM " + self.get_table() + ' WHERE ' + column + '=?', (cid,))

    def select_a_columns(self, column, cid):
        self.selectByColumn(column, column, cid)

    def select_columns(self, printColumns, selectedColumn, cid):
        self.cursor.execute("SELECT " + print_columns + " FROM " + self.get_table() + ' WHERE ' + selectedColumn + '=?', (cid,))

    def select_with_limit(self, printColumns, limit):
        self.cursor.execute("SELECT " + print_columns + " FROM " + self.get_table() + ' LIMIT ' + str(limit))

        
    def print_table(self):
        self.selectAll()
        for row in self.cursor.fetchall():
            print row

    def print_selection(self):
        for row in self.cursor.fetchall():
            for item in row:
                print item,
            print '\t'
        
    def print_a_row(self, column, cid):
        self.selectRow(column, cid)
        print self.cursor.fetchone()

    def print_rows(self, column, cid):
        self.selectRow(column, cid)
        for row in self.cursor.fetchall():
            print row

    def get_as_values(self, values):
        return 'VALUES' + str(values) + ''

    def get_columns(self):
        return str(self.columns)

    def insert(self, values):
        self.cursor.execute('INSERT INTO '
            + self.table + self.get_columns() + ' ' + self.get_as_values(values))

    def create_table(self, table, values):
        print self.cursor.execute('CREATE TABLE ' + table + ' ' + values)

    def join_tables(self, selection, table1, table2, key1, key2):
        return self.cursor.execute('SELECT ' + selection + ' FROM ' + table1
            + ' AS S CROSS JOIN ' + table2 + ' AS T WHERE S.' + key1 +'=T.' + key2)

    def execute(self, text):
        return self.cursor.execute(text).fetchall()

    def create_table(self, text):
        return self.cursor.executescript(text)

    def commit(self):
        self.conn.commit()

    def close(self):
        self.conn.close()
    
    def commit_and_close(self):
        self.commit()
        self.close()
