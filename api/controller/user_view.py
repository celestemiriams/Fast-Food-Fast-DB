"""
This module provides responses to url requests.
"""
from flask import jsonify, request
from flask.views import MethodView
from api.controller.user_logic import UserHandler
from api.models.user import User


class UserViews(MethodView):
    """
    This class contains methods that respond to various url end points.
    """

    user_handler = UserHandler()

    def get(self):
            """
            All orders posted 
            """
            token = request.headers.get('Authorization')
            if not token:
                return jsonify({"message": "Token is missing"}), 401

            decoded = User.decode_token(token)
            if isinstance(decoded, str):
                return User.decode_failure(decoded["error_message"])

            if "user_id" in decoded and  User.check_login_status(decoded["user_id"]):
                user_sql = """SELECT "users".username, orders.user_id, orders.item_id, orders.date, orders.orderstatus, orders.quantity FROM "orders" LEFT JOIN "users"\
                                ON(orders.user_id = "users".user_id) WHERE "orders".user_id = %s """
                sql_data = (decoded["user_id"], )
                return self.user_handler.return_order_history(user_sql, sql_data)   
            return jsonify({"message": "Please login"}), 401