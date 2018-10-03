"""
This module provides responses to url requests.
"""
from flask import jsonify, request
from flask.views import MethodView
from api.controller.order_logic import OrderHandler
from api.controller.user import User


class OrderViews(MethodView):
    """
    This class contains methods that respond to various url end points.
    """

    order_handler = OrderHandler()

    def get(self, order_id):
        """
        All orders posted 
        """
        token = request.headers.get('Authorization')
        if not token:
            return jsonify({"message": "Token is missing"}), 401

        decoded = User.decode_token(token)
        if isinstance(decoded, str):
            return User.decode_failure(decoded["error_message"])

        if User.check_login_status(decoded["user_id"]):
            if not order_id:
                # request_sql = """"SELECT orders.order_id,menu.item_name,menu.price,orders.quantity,orders.order_status,orders.date,users.username,users.phone_number
                #     FROM orders
                #     INNER JOIN menu ON menu.item_id = orders.item_id 
                #     INNER JOIN users ON users.user_id = orders.user_id
                #     ORDER BY orders.order_id;"""
                request_sql = "SELECT * FROM orders"
                sql_data = (decoded["user_id"])
                return self.order_handler.return_all_orders(request_sql, sql_data)
            return self.order_handler.return_single_order(order_id)
            
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
            
            if not request or not request.json:
                return jsonify({"status_code": 400, "data": str(request.data),
                                "error_message": "content not JSON"}), 400
            return self.order_handler.post_an_order(decoded["user_id"])
        return jsonify({"message": "Please login"}), 401

    def put(self, order_id):
        """
        This method handles put requests
        """
        token = request.headers.get('Authorization')
        if not token:
            return jsonify({"message": "Token is missing"}), 401
        decoded = User.decode_token(request.headers.get('auth_token'))
        if decoded["state"] == "Failure":
            return User.decode_failure(decoded["error_message"])
        if User.check_login_status(decoded["user_id"]):
            return self.order_handler.update_order_status(order_id)
        return jsonify({"message": "Please login"}), 401

