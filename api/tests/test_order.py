"""
This module contains tests for the api end points.
"""
from unittest import TestCase
from datetime import datetime
from flask import json
import psycopg2
from api.app import APP
from api.models.user import User
from api.models.order import Order
from api.models.database_connection import DatabaseAccess


class TestorderTestCase(TestCase):
    """
    Tests run for the api end pints.
    """

    user_test = User(12, "joyce", "joyce@gmail.com", "0771462657", "joyce@2")
    user_1 = User(123, "miriam", "miriam@gmail.com", "0702488995", "miriam@2")
    user_2 = User(235, "Vicky", "vic@vom.com", "0777897654", "vicky@1")

    order1 = Order(1, 2, 3)
    order2 = Order(10, 2, 1)
    order3 = Order(3, 5, 2)

    user1 = User("joyce","joyce@gmail.com", "0771462", "joyce@2")
    user2 = User("miriam", "miriam@gmail.com", "0772587", "miriam@1")
    user3 = User("admin", "admin1@gmail.com", "0789456789", "admin@add")


    def setUp(self):
        """Define test variables and initialize app."""
        APP.config['TESTING'] = True
        self.app = APP
        self.client = self.app.test_client
        DatabaseAccess.create_tables()
        DatabaseAccess.create_super_user()
        self.user1response = self.client().post('/api/v1/auth/signup/', data=json.dumps(
            self.user1.__dict__), content_type='application/json')
        
        self.client().post('/api/v1/auth/signup/', data=json.dumps(
            self.user2.__dict__), content_type='application/json')

        self.auth_header = {"Authorization":"Bearer "+ self.generate_token()}
        
        self.user1_auth_header =  {"Authorization":"Bearer "+ self.generate_user1_token()}
        
    
    def generate_user1_token(self):
        """
        This method gets a token to be used for authentication when
        making requests.
        """
        response = self.client().post(
            '/api/v1/auth/login/',
            data=json.dumps(dict(
                email=self.user1.email,
                password=self.user1.password
            )),
            content_type='application/json'
        )

        return json.loads(response.data)["auth_token"]

    def generate_token(self):
        """
        This method gets a token to be used for authentication when
        making requests.
        """
        response = self.client().post(
            '/api/v1/auth/login/',
            data=json.dumps(dict(
                email=self.user3.email,
                password=self.user3.password
            )),
            content_type='application/json'
        )

        return json.loads(response.data)["auth_token"]

    def test_post_creates_an_order(self):
        """
        This method tests for the creation of an order uses
        (POST request)
        """
        response = self.client().post('/api/v1/users/orders/', data=json.dumps(
            self.order3.__dict__), content_type='application/json',
                                      headers=self.user1_auth_header)
        self.assertEqual(response.status_code, 201)
        self.assertIn("Order", response.json)
        self.assertEqual("order successfully placed", response.json['message'])

    def test_api_gets_all_orders(self):
        """
        Test API can get all orders offers (GET request).
        """
        response = self.client().get('/api/v1/orders/',
                                     headers=self.auth_header)
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.json['Order'], list)
        self.assertIn("Available orders", response.json["message"])

    def test_api_gets_user_order_history(self):
        """
        Test API can get all orders made by a particular user
        """
        response = self.client().get('/api/v1/users/orders/',
                                     headers=self.user1_auth_header)
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.json['Order'], list)
        self.assertIn("Your orders", response.json["message"])

    def test_order_not_found(self):
        """
        Test API returns nothing when an order is not found
        """
        response = self.client().get('/api/v1/orders/20/',
                                     headers=self.auth_header)
        self.assertEqual(response.status_code, 200)
        self.assertEqual("No order available with id: 20", response.json['message'])

    def test_error_hander_returns_json(self):
        """
        Test API returns a json format response when the user hits
        a wrong api end point
        """
        response = self.client().get('/api/v1/orders/mm')
        self.assertEqual(response.status_code, 404)
        self.assertIsInstance(response.json, dict)
        self.assertEqual("The requested resource was not found on the server",
                         response.json["error_message"])
        self.assertEqual("http://localhost/api/v1/orders/mm",
                         response.json["url"])

    def test_non_json_data_not_sent(self):
        """
        This method tests that non json data is not sent
        """
        response = self.client().post('/api/v1/users/orders/', data=json.dumps(
            self.order1.__dict__), content_type='text/plain',
                                      headers=self.user1_auth_header)

        self.assertEqual(response.status_code, 400)
        self.assertTrue(response.json)
        self.assertEqual("content not JSON", response.json['error_message'])

    def test_empty_attributes_not_sent(self):
        """
        This method tests that data is not sent with empty fields
        """
        response = self.client().post('/api/v1/users/orders/', data=json.dumps(
            dict(user_id=3,
                 item_id = "",
                 quantity=4,)), content_type='application/json',
                                      headers=self.user1_auth_header)

        self.assertEqual(response.status_code, 400)
        self.assertTrue(response.json)
        self.assertEqual("Some fields are empty", response.json['error_message'])

    def test_partial_fields_not_sent(self):
        """
        This method tests that data with partial fields is not send
        on creating an order
        """
        response = self.client().post('/api/v1/users/orders/', data=json.dumps(
            dict(quantity=3)),content_type='application/json',
                                      headers=self.user1_auth_header)
        self.assertEqual(response.status_code, 400)
        self.assertEqual("some of these fields are missing",
                         response.json['error_message'])

    def test_edit_existing_order(self):
        """
        This method tests whether an update is made to an order
        A message of no order available is returned
        if an order doesnot exist.
        """
        response = self.client().put('/api/v1/orders/20/',
                                     data=json.dumps(dict(orderstatus="Processing")),
                                     content_type='application/json',
                                     headers=self.auth_header)
        self.assertEqual(response.status_code, 200)
        self.assertEqual("No order available with id: 20", response.json['message'])

    def test_invalid_token(self):
        """
        This method tests whether api rejects invalid token.
        """
        response = self.client().get('/api/v1/users/orders/',
                                     headers=({"Authorization": "bearer xxxxxvvvvvv"}))
        self.assertEqual(response.status_code, 401)
        self.assertEqual("Please login", response.json["message"])

    def test_token_missing(self):
        """
        This method tests whether api rejects orders
        with missing tokens.
        """
        response = self.client().get('/api/v1/users/orders/')
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
            """DROP TABLE IF EXISTS "users" CASCADE;""",
            """DROP TABLE IF EXISTS "orders" CASCADE;""",
            """DROP TABLE IF EXISTS "menu" CASCADE;""")
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


    
