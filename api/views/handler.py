"""
This module handles Errors when a user hits a wrong api end point.
"""
from flask import jsonify, request


class ErrorHandler(object):
    """
    This Class handles request errors when a user sends a wrong url.
    """
    @staticmethod
    def url_not_found(status_code=None):
        """
        This Method returns a formatted 404 error message in json format.
        :return: response
        """
        if status_code:

            message = {
                "error_message": "The requested resource was not found on the server",
                "status_code": 404,
                "url":  request.url
            }
            response = jsonify(message)
            response.status_code = 404
        return response