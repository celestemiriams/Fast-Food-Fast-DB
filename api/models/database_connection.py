"""
This module handles the database set up
"""
import os
import psycopg2
from flask import current_app as app

class DatabaseAccess(object):
    """
    This class contains methods to create a database connection
    """

    @staticmethod
    def database_connection():
        """
        This method creates a connection to the database
        """
        #from api.app import APP

        #if not APP.config['TESTING']:
        connection = psycopg2.connect(
                """dbname='fast-food-fast' user='celestemiriams' host='localhost'\
                password='lutwama@2' port='5432'"""
            )
        return connection

        # connection = psycopg2.connect(
        #     "dbname='testdb' user='celestemiriams' host='localhost' password='lutwama@2' port='5432'"
        # )
        # return connection
        

    
    @staticmethod
    def create_tables():
        """
        This method creates tables in the PostgreSQL database.
        It connects to the database and creates tables one by one
        """
        connection = psycopg2.connect(
                """dbname='fast-food-fast' user='celestemiriams' host='localhost'\
                password='lutwama@2' port='5432'"""
            )
        commands = (
            # """DROP TABLE IF EXISTS users CASCADE """,
            # """DROP TABLE IF EXISTS menu CASCADE""",
            # """DROP TABLE IF EXISTS orders CASCADE""",

            """
            CREATE TABLE IF NOT EXISTS "users" (
                    user_id SERIAL PRIMARY KEY, username VARCHAR(25) NOT NULL,
                    email VARCHAR(50) UNIQUE NOT NULL, phonenumber INTEGER NOT NULL,
                    usertype BOOLEAN NOT NULL DEFAULT FALSE, password VARCHAR(255) NOT NULL,
                    is_loggedin BOOLEAN DEFAULT FALSE
                )
            """,
            """
            CREATE TABLE IF NOT EXISTS "menu" (
                    item_id SERIAL PRIMARY KEY, item_category VARCHAR(50) NOT NULL,
                    item_name VARCHAR(50) NOT NULL, price INTEGER NOT NULL
                )
            """,
            """
            CREATE TABLE IF NOT EXISTS "orders" (
                    order_id SERIAL PRIMARY KEY, user_id INTEGER NOT NULL,
                    item_id INTEGER NOT NULL, date TIMESTAMP DEFAULT NOW(),
                    orderstatus VARCHAR(25) NOT NULL DEFAULT 'new',
                    quantity INTEGER NOT NULL,
                    FOREIGN KEY (user_id) REFERENCES "users" (user_id)
                    ON UPDATE CASCADE ON DELETE CASCADE,
                    FOREIGN KEY (item_id) REFERENCES "menu" (item_id)
                    ON UPDATE CASCADE ON DELETE CASCADE
                )
            """,)
        try:
            cursor = connection.cursor()
            for command in commands:
                cursor.execute(command)
            connection.commit()
            cursor.close()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        finally:
            if connection is not None:
               connection.close()

db = DatabaseAccess()
db.create_tables()

        