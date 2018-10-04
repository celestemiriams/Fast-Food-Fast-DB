"""
This module handles specific requests made
on the API end points
"""
from flask import jsonify, request
from api.controller.user import User
from api.models.database_transaction import DbTransaction
from api.controller.error_messages import ErrorMessage


class UserHandler(object):
    """
    This class contains methods that handle specific
    requests made to the menu end points
    """

    error_message = ErrorMessage()

    def return_order_history(self, sql_statement, data=None):
        """
        This method returns orders made by a specific user
        """

        sql = sql_statement
        if data is not None:
            order_list = DbTransaction.retrieve_all(sql, data)
        else:
            order_list = DbTransaction.retrieve_all(sql)

        _order_ = []
        for order_ in order_list:
                order_dict = {
                "username": order_[0],
                "user_id": order_[1],
                "item_id": order_[2],
                "date": order_[3],
                "order_status": order_[4],
                "quantity": order_[5]
                }
                _order_.append(order_dict)
        return jsonify({"message": "Your orders",
                        "Order": _order_})

