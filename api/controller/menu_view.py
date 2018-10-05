"""
This module provides responses to url requests.
"""
from flask import jsonify, request
from flask.views import MethodView
from api.controller.menu_logic import MenuHandler
from api.models.user import User


class MenuViews(MethodView):
    """
    This class contains methods that respond to various url end points.
    """

    menu_handler = MenuHandler()

    def get(self):
        """
        All menu options posted are returned 
        """
        token = request.headers.get('Authorization')
        if not token:
            return jsonify({"message": "Token is missing"}), 401

        decoded = User.decode_token(token)
        if isinstance(decoded, str):
            return User.decode_failure(decoded["error_message"])

        if "user_id" in decoded and User.check_login_status(decoded["user_id"]):
                request_sql = "SELECT * FROM menu"
                sql_data = (decoded["user_id"])
                print(sql_data)
                return self.menu_handler.return_menu_items(request_sql, sql_data)
        return jsonify({"message": "Please login"}), 401

    def post(self):
        """"
        Handles post requests
        """
        token = request.headers.get('Authorization')
        if not token:
            return jsonify({"message": "Token is missing"}), 401
        decoded = User.decode_token(token)
        if decoded["state"] == "Failure":
            return User.decode_failure(decoded["error_message"])
        if User.check_login_status(decoded["user_id"]):
            userId = decoded["user_id"]
            is_admin = User.get_user_by_id(userId)
            if is_admin:
                if not request or not request.json:
                    return jsonify({"status_code": 400, "data": str(request.data),
                                    "error_message": "content not JSON"}), 400
                return self.menu_handler.post_menu_option(decoded["user_id"])
            return jsonify({"message": "Not admin"})
        return jsonify({"message": "Please login"}), 401

