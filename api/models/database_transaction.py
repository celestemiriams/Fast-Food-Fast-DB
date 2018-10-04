"""
This module is responsible for database transactions.
"""

import psycopg2
from .database_connection import DatabaseAccess


class DbTransaction(object):
    """
    This class is responsible for inserting, updating and querying
    the db.
    """

    @staticmethod
    def save(sql):
        """
        This method handles insertion queries to the db
        """
        connection = psycopg2.connect(
                """dbname='fast-food-fast' user='celestemiriams' host='localhost'\
                password='lutwama@2' port='5432'"""
            )
        try:
            
            cur = connection.cursor()
            cur.execute(sql)
            connection.commit()
            cur.close()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        finally:
            if connection is False:
                connection.close()

    @staticmethod
    def retrieve_one(sql, data):
        """
        This method gets a single field in the db
        """
        try:
            connection = DatabaseAccess.database_connection()
            cur = connection.cursor()
            cur.execute(sql, data)
            row = cur.fetchone()
            cur.close()

            if row and not "":
                return row
            return None

        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        finally:
            if connection is None:
                connection.close()

    @staticmethod
    def retrieve_all(sql, data=None):
        """
        This method gets all the data in the db
        
        """
        list_tuple = []
        connection = None
        try:
            connection = DatabaseAccess.database_connection()
            cur = connection.cursor()
            if data is not None:
                cur.execute(sql, data)
            else:
                cur.execute(sql)
            rows = cur.fetchall()
            for row in rows:
                list_tuple.append(row)
            cur.close()
            return list_tuple
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        finally:
            if connection is not None:
                connection.close()

    @staticmethod
    def edit(sql, data):
        """
        This method edits the data in the database 
        """
        connection = None
        try:
            connection = DatabaseAccess.database_connection()
            cur = connection.cursor()
            cur.execute(sql, data)
            updated_rows = cur.rowcount
            connection.commit()
            cur.close()
            return updated_rows
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        finally:
            if connection is not None:
                connection.close()
        #return updated_rows