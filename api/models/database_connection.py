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

        connection = psycopg2.connect(
                """dbname='fast-food-fast' user='celestemiriams' host='localhost'\
                password='lutwama@2' port='5432'"""
            )
        return connection
        

    
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
            """
            CREATE TABLE "user" (
                    user_id SERIAL PRIMARY KEY, username VARCHAR(25) NOT NULL,
                    email VARCHAR(25) UNIQUE NOT NULL, phonenumber INTEGER NOT NULL,
                    usertype VARCHAR(25) NOT NULL, password VARCHAR(255) NOT NULL
                )
            """,
            """
            CREATE TABLE "menu" (
                    item_id SERIAL PRIMARY KEY, itemname VARCHAR(50) NOT NULL,
                    itemcategory VARCHAR(50) NOT NULL, price INTEGER NOT NULL
                )
            """,
            """
            CREATE TABLE "order" (
                    order_id SERIAL PRIMARY KEY, user_id INTEGER NOT NULL,
                    item_id INTEGER NOT NULL, date TIMESTAMP NOT NULL,
                    orderstatus VARCHAR(25) NULL,
                    FOREIGN KEY (user_id) REFERENCES "user" (user_id)
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

    # def insert_user_data(self,username, email, password ):
    #     connection = psycopg2.connect(
    #             """dbname='stackoverflow' user='celestemiriams' host='localhost'\
    #             password='lutwama@2' port='5432'"""
    #         )
    #     cursor = connection.cursor()
    #     """inserting data"""
    #     user_query = "INSERT INTO user (username, email, password) VALUES\
    #      ('{}', '{}', '{}');".format(username, email, password)
    #     cursor.execute(user_query)
    #     connection.commit()
    #     connection.close()

db = DatabaseAccess()
db.create_tables()

        