import mysql.connector
from mysql.connector import pooling
from commons.exceptions.db import *
from settings import DB_MYSQL_CONFIG, MYSQL_DEFAULT_CHARACTER

class MySQLClient:

    def __init__(self):
        self.pool = pooling.MySQLConnectionPool(**DB_MYSQL_CONFIG)

    def get_connection_and_cursor(self):
        conn = self.pool.get_connection()
        return conn, conn.cursor()

    @catch_exceptions(mysql.connector.Error)
    def create_database(self, database_name):
        conn, cursor = self.get_connection_and_cursor()
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {database_name} default character set {MYSQL_DEFAULT_CHARACTER}")
    
    @catch_exception(mysql.connector.IntegrityError)
    def create_table(self, table_name, column_info):
        conn, cursor = self.get_connection_and_cursor()
        create_table_sql = f"CREATE TABLE IF NOT EXISTS {table_name} ({column_info})"
        cursor.execute(create_table_sql)

    @catch_exception(mysql.connector.IntegrityError)
    def insert(self, table_name, column_names, values):
        conn, cursor = self.get_connection_and_cursor()
        insert_sql = f"INSERT INTO {table_name} ({','.join(column_names)}) VALUES ({','.join(['?' for v in values])})"
        cursor.execute(insert_sql, values)
        conn.commit()

    @catch_exception(mysql.connector.IntegrityError)
    def select(self, table_name, conditions=None):
        conn, cursor = self.get_connection_and_cursor()
        select_sql = f"SELECT * FROM {table_name}"
        if conditions:
            select_sql += " WHERE " + conditions 
        cursor.execute(select_sql)
        return cursor.fetchall()

    @catch_exception(mysql.connector.IntegrityError)
    def update(self, table_name, column_name, value, conditions):
        conn, cursor = self.get_connection_and_cursor()
        update_sql = f"UPDATE {table_name} SET {column_name}=? WHERE {conditions}"
        cursor.execute(update_sql, (value,))
        conn.commit()
    
    @catch_exception(mysql.connector.IntegrityError)
    def delete(self, table_name, conditions):
        conn, cursor = self.get_connection_and_cursor()
        delete_sql = f"DELETE FROM {table_name} WHERE {conditions}"
        cursor.execute(delete_sql)
        conn.commit()