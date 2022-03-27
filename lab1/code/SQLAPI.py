import re
import ERROR
import pymysql
import pymysql.cursors as cursors
from pymysql.err import OperationalError

class SQLSocket():
    def __init__(self, host='localhost', user='root', password=None, database=None):
        self.__sql_socket = None
        self.host = host
        self.user = user
        self.password = password
        self.database = database

    def __del__(self):
        if self.__sql_socket is not None:
            self.__sql_socket.close()

    def __SendQuery(self, query):
        with self.__sql_socket.cursor() as cursor:
            cursor.execute(query)
            return cursor.fetchall()

    def __SendChange(self, query):
        with self.__sql_socket.cursor() as cursor:
            cursor.execute(query)
        self.__sql_socket.commit()

    def Connect(self):
        error = ERROR.ACCEPT
    
        try:
            self.__sql_socket = pymysql.connect(host=self.host, 
                                                user=self.user, 
                                                passwd=self.password, 
                                                db=self.database,
                                                charset='utf8mb4', 
                                                cursorclass=cursors.DictCursor)
        except OperationalError as e:
            err_message = str(e)
            if re.search('Can\'t connect to MySQL server on', err_message):
                error = ERROR.HOST_ERROR
            elif re.search('Access denied for user', err_message):
                error = ERROR.USER_OR_PASSWORD_ERROR
            elif re.search('Unknown database', err_message):
                error = ERROR.DATABASE_ERROR
        finally:
            return error
    
    def Query(self, query):
        result = self.__SendQuery(query)
        return result
    
    def Insert(self, query):
        error = ERROR.ACCEPT

        try:
            self.__SendChange(query)
        except Exception as e:
            err_message = str(e)
            if re.search('Table .* doesn\'t exist', err_message):
                error = ERROR.TABELE_NOT_EXIST
            elif re.search('Column count doesn\'t match value count at row', err_message):
                error = ERROR.INSERT_VALUE_ERROR
            elif re.search('Duplicate entry', err_message):
                error = ERROR.DUPLICATE_ENTRY_ERROR
            elif re.search('Incorrect integer value', err_message):
                error = ERROR.TYPE_ERROR
            print(err_message)
        finally:
            return error
    
    def Delete(self, query):
        error = ERROR.ACCEPT

        try:
            self.__SendChange(query)
        except Exception as e:
            err_message = str(e)
            if re.search('Cannot delete or update a parent row', err_message):
                error = ERROR.DELETE_OR_UPDATE_PARENT_ROW
            print(err_message)
        finally:
            return error