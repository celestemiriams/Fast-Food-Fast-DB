"""
This module returns meaningful error messages.
"""
from flask import jsonify


class ErrorMessage(object):
    """
    This class contains methods to that return error messages.
    """

    def fields_missing_information(self, answer_data):
        """
        This method a response when some fields in the data sent are missing
        """
        return jsonify({"status": "failure",
                        "status_code": 400, "data": answer_data,
                        "error_message": "Some fields are empty"}), 400

    def request_missing_fields(self):
        """
        This method returns an error message that some fields are missing
        """
        return jsonify({"status": "failure",
                        "error_message": "some of these fields are missing"}), 400

    def no_order_available(self, order_id):
        """
        This method returns a JSON response with a message of no order
        """
        return jsonify({"status": "failure",
                        "message": "No order available with id: " + str(order_id)}), 200

