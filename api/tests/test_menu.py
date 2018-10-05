"""
This module contains tests for the api end points.
"""
from unittest import TestCase
from datetime import datetime
from flask import json
import psycopg2
from api.app import create_app
from api.models.user import User
from api.models.menu import Menu
from api.models.database_connection import DatabaseAccess


class TestorderTestCase(TestCase):
    """
    Tests run for the api end pints.
    """

    user_test = User(12, "joyce", "joyce@gmail.com", "0771462657", "joyce@2")
    user_1 = User(123, "miriam", "miriam@gmail.com", "0702488995", "miriam@2")
    user_2 = User(235, "Vicky", "vic@vom.com", "0777897654", "vicky@1")

    menu1 = Menu("local food", "matooke and fish", 7000)
    menu2 = Menu("snack", "chips and chicken", 9000)
    menu3 = Menu("pizza", "vegetable pizza", 15000)

    user1 = User("joyce","joyce@gmail.com", "0771462", "joyce@2")
    user2 = User("miriam", "miriam@gmail.com", "0772587", "miriam@1")

    def setUp(self):
        """Define test variables and initialize app."""
        config_name = 'testing'
        self.app = create_app(config_name)
        self.client = self.app.test_client
        DatabaseAccess.create_tables()
        self.client().post('/api/v1/auth/signup/', data=json.dumps(
            self.user1.__dict__), content_type='application/json')
        self.client().post('/api/v1/auth/signup/', data=json.dumps(
            self.user2.__dict__), content_type='application/json')
        self.client().post('/api/v1/menu/', data=json.dumps(
            self.menu1.__dict__), content_type='application/json',
                           headers=({"auth_token": self.generate_token()}))
        self.client().post('/api/v1/menu/', data=json.dumps(
            self.menu2.__dict__), content_type='application/json',
                           headers=({"auth_token": self.generate_token()}))

    def generate_token(self):
        """
        This method gets a token to be used for authentication when
        making requests.
        """
        response = self.client().post(
            '/api/v1/auth/login/',
            data=json.dumps(dict(
                email_address=self.user1.email,
                password=self.user1.password
            )),
            content_type='application/json'
        )
        return response.json["auth_token"]

    def test_api_gets_menu(self):
        """
        Test API can get a menu (GET request).
        """
        response = self.client().get('/api/v1/menu/',
                                     headers=({"auth_token": self.generate_token()}))
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.json['orders'], list)
        self.assertIn("results retrieved successfully", response.json["message"])


    def test_error_hander_returns_json(self):
        """
        Test API returns a json format response when the user hits
        a wrong api end point
        """
        response = self.client().get('/api/v1/menu/mm')
        self.assertEqual(response.status_code, 404)
        self.assertIsInstance(response.json, dict)
        self.assertEqual("The requested resource was not found on the server",
                         response.json["error_message"])
        self.assertEqual("http://localhost/api/v1/menu/mm",
                         response.json["url"])

    def test_post_adds_a_menu_option(self):
        """
        This method tests for the addition of a menu option
        (POST request)
        """
        response = self.client().post('/api/v1/menu/', data=json.dumps(
            self.menu3.__dict__), content_type='application/json',
                                      headers=({"auth_token": self.generate_token()}))

        self.assertEqual(response.status_code, 201)
        self.assertIn("menu", response.json)
        self.assertEqual("Menu option added successfully", response.json['message'])
        self.assertTrue(response.json['order'])

    def test_non_json_data_not_sent(self):
        """
        This method tests that non json data is not sent
        """
        response = self.client().post('/api/v1/menu/', data=json.dumps(
            self.menu1.__dict__), content_type='text/plain',
                                      headers=({"auth_token": self.generate_token()}))

        self.assertEqual(response.status_code, 400)
        self.assertTrue(response.json)
        self.assertEqual("content not JSON", response.json['error_message'])

    def test_empty_attributes_not_sent(self):
        """
        This method tests that data is not sent with empty fields
        """
        response = self.client().post('/api/v1/menu/', data=json.dumps(
            dict(item_category="",
                 item_name = "",
                 price=4000,)), content_type='application/json',
                                      headers=({"auth_token": self.generate_token()}))

        self.assertEqual(response.status_code, 400)
        self.assertTrue(response.json)
        self.assertEqual("Some fields are empty", response.json['error_message'])

    def test_partial_fields_not_sent(self):
        """
        This method tests that data with partial fields is not send
        on creating an order
        """
        response = self.client().post('/api/v1/menu/', data=json.dumps(
            dict(item_category="pizza", item_name= "mashroom pizza")),content_type='application/json',
                                      headers=({"auth_token": self.generate_token()}))
        self.assertEqual(response.status_code, 400)
        self.assertEqual("some of these fields are missing",
                         response.json['error_message'])

    def test_invalid_token(self):
        """
        This method tests whether api rejects invalid token.
        """
        response = self.client().get('/api/v1/menu/',
                                     headers=({"auth_token": "xxxxxvvvvvv"}))
        self.assertEqual(response.status_code, 401)
        self.assertEqual("Invalid token. Please log in again.", response.json["message"])

    def test_token_missing(self):
        """
        This method tests whether api rejects menu options
        with missing tokens.
        """
        response = self.client().get('/api/v1/menu/')
        self.assertEqual(response.status_code, 401)
        self.assertEqual("Token is missing", response.json["message"])

    def test_login_status(self):
        """
        This method tests the status of a user when logged in
        """
        response = User.check_login_status(1)
        self.assertEqual(True, response)

    def tearDown(self):
        sql_commands = (
            """DROP TABLE IF EXISTS "user" CASCADE;""",
            """DROP TABLE IF EXISTS "ride" CASCADE;""",
            """DROP TABLE IF EXISTS "request" CASCADE;""")
        conn = None
        try:
            conn = DatabaseAccess.database_connection()
            cur = conn.cursor()
            for sql_command in sql_commands:
                cur.execute(sql_command)
            cur.close()
            conn.commit()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        finally:
            if conn is not None:
                conn.close()


    
