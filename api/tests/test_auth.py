"""
This module contains tests for user account creation
and signing in.
"""
import uuid
from unittest import TestCase
from flask import json
import psycopg2
from api.models.user import User
from api.app import create_app
from api.models.database_connection import DatabaseAccess


class TestUserAuthTestCase(TestCase):
    """
    Tests run for the api end pints.
    """
    user1 = User("miriam","miriam@gmail.com","0702345678", "lutwama@2")
    empty_user = User("", "", "", "")
    def setUp(self):
        """
        Define test variables and initialize app.
        """
        config_name = 'testing'
        self.app = create_app(config_name)
        self.client = self.app.test_client
        DatabaseAccess.create_tables()

    def test_app_is_development(self):
        """
        This method tests configuration variables such that they are set correctly
        """
        self.assertNotEqual(self.app.config['SECRET_KEY'], "my-food-delivery-service-app")
        self.assertFalse(self.app.config['DEBUG'] is True)
        self.assertTrue(self.app.config['TESTING'] is True)

    def test_user_registration(self):
        """
        Test a user is successfully created through the api
        """
        response = self.client().post('/api/v1/auth/signup/', data=json.dumps(
            self.user1.__dict__), content_type='application/json')

        self.assertEqual(response.status_code, 201)
        self.assertTrue(response.content_type == 'application/json')
        self.assertIn("user", response.json)
        self.assertEqual("Successfully registered", response.json['message'])
        self.assertTrue(response.json['user'])

    def test_content_type_not_json(self):
        """
        Test that the content type that is not application/json
        """
        response = self.client().post('/api/v1/auth/signup/', data=json.dumps(
            self.user1.__dict__), content_type='text/plain')

        self.assertEqual(response.status_code, 400)
        self.assertEqual("Failed Content-type must be json", response.json['error_message'])

    def test_empty_attributes_not_sent(self):
        """
        This method tests that data is not sent with empty fields
        """
        response = self.client().post('/api/v1/auth/signup/', data=json.dumps(
            self.empty_user.__dict__), content_type='application/json')

        self.assertEqual(response.status_code, 400)
        self.assertTrue(response.json)
        self.assertEqual("Some fields are not defined", response.json['error_message'])

    def test_partial_fields_not_sent(self):
        """
        This method tests that data with partial fields is not send
        """
        response = self.client().post('/api/v1/auth/signup/', data=json.dumps(
            dict(username=self.user1.username, email=self.user1.email)),
                 content_type='application/json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual("Some fields are missing, all fields are required",
                         response.json['error_message'])

    def test_user_login(self):
        """
        Test for login of a registered user
        """
        self.client().post('/api/v1/auth/signup/', data=json.dumps(
            self.user1.__dict__), content_type='application/json')

        response = self.client().post(
            '/api/v1/auth/login/',
            data=json.dumps(dict(
                email=self.user1.email,
                password=self.user1.password
            )),
            content_type='application/json'
        )

        self.assertTrue(response.json['status'] == 'success')
        self.assertTrue(response.json['message'] == 'Successfully logged in.')
        self.assertTrue(response.json['auth_token'])
        self.assertTrue(response.content_type == 'application/json')
        self.assertEqual(response.status_code, 200)

    def tearDown(self):
        sql_commands = (
            """DROP TABLE IF EXISTS "users" CASCADE;""",
            """DROP TABLE IF EXISTS "menu" CASCADE;""",
            """DROP TABLE IF EXISTS "orders" CASCADE;""")
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
                