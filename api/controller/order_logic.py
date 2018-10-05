"""
This module handles specific requests made
on the API end points
"""
from flask import jsonify, request
from api.controller.order import Order
from api.models.database_transaction import DbTransaction
from api.controller.error_messages import ErrorMessage


class OrderHandler(object):
    """
    This class contains methods that handle specific
    requests made to the order end points
    """

    error_message = ErrorMessage()

    def return_all_orders(self, sql_statement, data=None):
        """
        This method returns order details
        """
        sql = sql_statement
        order_list = []

        if data is not None:
            order_list = DbTransaction.retrieve_all(sql, data)
        else:
            order_list = DbTransaction.retrieve_all(sql)

        _order_ = []
        for order_ in order_list:
            order_dict = {
                "order_id": order_[0],
                "user_id": order_[1],
                "item_id": order_[2],
                "date": order_[3],
                "order_status": order_[4],
                "quantity": order_[5]
            }
            _order_.append(order_dict)
        return jsonify({"message": "Available orders",
                        "Order": _order_})

    def return_single_order(self, order_id):
        """
        This method returns order details
        """
        single_order_sql =  " SELECT * FROM orders WHERE order_id = %s"
        order_turple = DbTransaction.retrieve_one(single_order_sql, (order_id, ))

        if order_turple is not None:
            order_id = order_turple[0]
            user_id = order_turple[1]
            item_id = order_turple[2]
            quantity = order_turple[3]
            order_status = order_turple[4]
            
            return jsonify({"Status code": 200, "order": {
                "order_id": order_id,
                "user_id": user_id,
                "item_id": item_id,
                "quantity": quantity,
                "order_status": order_status

            }, "message": "result retrieved successfully"})
        return self.error_message.no_order_available(order_id)

    def post_an_order(self, user_id):
        """
        This method allows a user to place an order
        """
        keys = ("item_id","quantity")
        if not set(keys).issubset(set(request.json)):
            return self.error_message.request_missing_fields()

        request_condition = [
            request.json["item_id"],
            request.json["quantity"]
            ]

        if not all(request_condition):
            return self.error_message.fields_missing_information(request.json)
        user = DbTransaction.retrieve_one(
            """SELECT user_id FROM users WHERE user_id = %s""",
            (user_id, ))
        user_string = user[0]
        if user_string is None:
            return jsonify({"message": "user doesnot exist"})
        item_id = request.json['item_id']
        quantity = request.json['quantity']
    
        order = Order(user_string, item_id, quantity)
        order.save_order()
        return jsonify({"status_code": 201, "Order": order.get_order_information(),
                        "message": "order successfully placed"}), 201

    def update_order_status(self, order_id):
        if request.content_type == 'application/json':
            db_order_id = DbTransaction.retrieve_one(
                    """SELECT "order_id" FROM "orders" WHERE "order_id" = %s""",
                    (order_id, ))
            
            if db_order_id:
                    edit_sql = """UPDATE orders SET orderstatus = %s
                    WHERE order_id = %s"""
                    edit_data = (request.json["orderstatus"], order_id)
                    updated_rows = DbTransaction.edit(edit_sql, edit_data)
                    return jsonify({"status": "success",
                                    "message": "order " + request.json["orderstatus"] + " successfully.\
                                    " + str(updated_rows) + " row(s) updated"}), 200
            return self.error_message.no_order_available(order_id)
        return jsonify({"Status": "failure", "message": "Content-type must be JSON"}), 400
            
