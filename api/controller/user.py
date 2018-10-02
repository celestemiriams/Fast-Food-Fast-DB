"""
This module is a usermodel
"""
import jwt
import datetime
from flask import jsonify
from api.models.database_transaction import DbTransaction
#from api.app import APP


class User(object):
    """
    This class represents a User entity
    """
    def __init__(self, *args):
        self.username = args[0]
        self.email = args[1]
        self.phonenumber = args[2]
        self.password = args[3]

    def save_user(self):
        """
        This method saves a user instance in the database.
        """
        self.username
        self.email
        self.phonenumber 
        self.password
        user_sql = "INSERT INTO users (username, email, phonenumber, password) VALUES\
        ('{}', '{}', {}, '{}');".format(self.username, self.email, self.phonenumber, self.password)
        DbTransaction.save(user_sql)


    def return_user_details(self):
        """
        This method returns the details of the user
        in json format.
        """ 
        return {
            "username": self.username,
            "email": self.email,
            "phonenumber": self.phonenumber 
        }

    @staticmethod
    def encode_token(user_id):
        """
        Generates the Auth Token
        :return: string
        """
        
        try:
            token = jwt.encode({"user_id": user_id,
                                "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=2880)},
                               "my-food-delivery-service-application")
            return token
        except Exception as error:
            raise error

    @staticmethod
    def decode_token(auth_token):
        """
        Decodes the auth token and returns the user public id
    
        """
        dtoken=auth_token.split(' ')[1]
        try:
            token = jwt.decode(dtoken, "my-food-delivery-service-application")
            return {"user_id": token["user_id"],
                    "state": "Success"}
              
        except jwt.ExpiredSignatureError:
            return {"error_message": "Signature expired. Please log in again.",
                    "state": "Failure"}
        except jwt.InvalidTokenError:
            return {"error_message": "Invalid token. Please log in again.",
                    "state": "Failure"}

    @staticmethod
    def decode_failure(message):
        """
        This method returns an error message when an error is
        encounterd on decoding the token
        """
        return jsonify({"message": message}), 401

    @staticmethod
    def check_login_status(user_id):
        """
        This method checks whether a user is logged in or not
        If a user is logged in, it returns true and returns
        false if a user is not logged in
        """
        is_loggedin = DbTransaction.retrieve_one(
            """SELECT "is_loggedin" FROM "users" WHERE "user_id" = %s""",
            (user_id, ))
        if is_loggedin[0]:

            return True
        return False