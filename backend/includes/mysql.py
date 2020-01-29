#encoding: utf-8

import datetime, time
import pymysql


class Database:
    #connects to *database* at *host* with *user* and *password*
    def __init__(self, host, database, user, password, logger):
        self.host = host
        self.database = database
        self.user = user
        self.password = password 
        self.tables = [0]
        self.logger = logger

    #connects to the db
    def connect(self):
        try:
            self.con = pymysql.connect(user=self.user, password=self.password, db=self.database, host=self.host, charset='utf8mb4', cursorclass=pymysql.cursors.DictCursor)
            self.cursor = self.con.cursor()
            return True
        except Exception as e:
            self.logger.error('Could not connect to %s at %s. Got error: %s', self.database, self.host, e)
            print (e)
            return False

    #closes the db connection
    def close(self):
        try: 
            self.con.close()
            return True
        except Exception as e:
            self.logger.error('Could not close %s at %s. Got error: %s', self.database, self.host, e)
            return False

    #creates the table *name* with colums *colums*
    #   name = 'tablename'
    #   colums = ['name VARCHAR(50)', 'age INT(3)']
    def createTable(self, name, colums):
        sql_createTable = """CREATE TABLE IF NOT EXISTS {} (id INTEGER PRIMARY KEY AUTO_INCREMENT, time TIMESTAMP""".format(name)
        for colum in colums:
            sql_createTable += """, {}""".format(colum)
        sql_createTable += """);"""
        
        try:
            self.cursor.execute(sql_createTable)
            self.con.commit()
            self.logger.debug('Successfuly created Table %s in %s at %s.', name, self.database, self.host)
        except Exception as e:
            self.logger.error('Could not create Table %s in %s at %s. Got error: %s', name, self.database, self.host, e)
            return False
        
        #check if the table is in the db
        for table in self.showTables():
            tablename = 'Tables_in_{}'.format(self.database)

            if (table[tablename] == name):
                return True
        
        self.logger.error('Could not find created table at %s.', self.database)
        return False

    #inserts *values* into the *table* from the db
    #   table = 'tablename'
    #   values = [['name', 'yourname'], ['age', 'yourage']]
    def insertInto(self, table, values):
        sql_insertInto = """INSERT INTO {} (time""".format(table)
        for colum in values:
            sql_insertInto += """,{}""".format(colum[0])

        datetimeNow = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        sql_insertInto += """) values ('{}'""".format(datetimeNow)

        for value in values:
            sql_insertInto += """,'{}'""".format(value[1])

        sql_insertInto += """);"""

        try:
            self.cursor.execute(sql_insertInto)
            self.con.commit()
            self.logger.debug('Inserted values into %s at %s: %s', table, self.database, sql_insertInto)
            return True
        except Exception as e:
            self.logger.error('Inserting into Table %s at %s failed. Got error: %s | Statement: %s', table, self.database, e, sql_insertInto)
            return False

    #updates *values* in *table* where *conditions*
    #   values = [['name', 'yourname], ['age', 'yourage']]
    #   table = 'tablename'
    #   conditions = "id = 1 && (name = 'yourname' || age = 'yourage')"
    def update(self, values, table, conditions):
        sql_update = """UPDATE {} SET """.format(table)

        for value in values:
            sql_update += """{} = {},""".format(value[0], value[1])

        sql_update = sql_update[:-1]

        sql_update += """ WHERE {};""".format(conditions)

        try:
            self.cursor.execute(sql_update)
            self.logger.debug('Updated sth in %s at %s: %s', table, self.database, sql_update)
            return True
        except Exception as e:
            self.logger.error('Could not update sth in %s at %s. Got error: %s', table, self.database, e)
            return False

    #deletes everything where *conditions* in *table*
    #   table = 'tablename'
    #   conditions = "id = 1 && name = 'yourname'"
    def delete(self, table, conditions):
        sql_delete = """DELETE FROM {} WHERE {}""".format(table, conditions)

        try:
            self.cursor.execute(sql_delete)
            self.logger.debug('Deleted sth in %s at %s: %s', table, self.database, sql_delete)
            return True
        except Exception as e:
            self.logger.error('Could not delete sth in %s at %s. Got error: %s', table, self.database, e)
            return False

    #returns all tables in db Format: 
    #   return = [{'Tables_in_dbname': 'tablename'}, {...}]
    def showTables(self):
        try:
            self.cursor.execute('SHOW TABLES')
            tables = self.cursor.fetchall()
            return tables
        except Exception as e:
            self.logger.error('Getting tables from %s failed. Got error: %s', self.database, e)
            return False
    
    #deletes the table *table*
    #   table = 'tablename'
    def dropTable(self, table):
        try:
            sql_dropTable = 'DROP TABLE {}'.format(table)
            self.cursor.execute(sql_dropTable)
            return True
        except Exception as e:
            self.logger.error('Could not delete table %s at %s. Got error: %s', table, self.database, e)
            return False

     #selects *values* from the *table* from the db
    #   table = 'tablename'
    #   selection = 'name, prename, birth'
    #   conditions = 'id > 0'
    def selectFrom(self, table, selection, conditions):
        sql_selectFrom = """SELECT {} FROM {} WHERE {}""".format(selection, table, conditions)

        try:
            self.cursor.execute(sql_selectFrom)
            selects = self.cursor.fetchall()
            self.con.commit()
            self.logger.debug('Selected %s from %s where %s', selection, table, conditions)
            return selects
        except Exception as e:
            self.logger.error('Select from Table %s at %s failed. Got error: %s | Statement: %s', table, self.database, e, sql_selectFrom)
            print (e)
            return False

    #checkf is entry exists
    #   tablename = 'tablename'
    #   conditons = 'id = 0'
    def checkIfExists(self, tablename, conditions):
        select = self.selectFrom(tablename, 'id', conditions)

        print (select)

        try:
                if len(select) > 0:
                    return True
        except:
            return False
        return False

    def execute(self, query):
        try:
            self.cursor.execute(query)
            selects = self.cursor.fetchall()
            self.con.commit()
            self.logger.debug('Executed: %s', query)
            return selects
        except Exception as e:
            self.logger.error('Execution failed: %s', query)
            print (e)
            return False

    def lastId(self):
        return self.con.insert_id()




