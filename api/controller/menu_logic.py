"""
This module handles specific requests made
on the API end points
"""
from flask import jsonify, request
from api.controller.menu import Menu
from api.models.database_transaction import DbTransaction
from api.controller.error_messages import ErrorMessage


class MenuHandler(object):
    """
    This class contains methods that handle specific
    requests made to the menu end points
    """

    error_message = ErrorMessage()

    def return_menu_items(self, sql_statement, data=None):
        """
        This method returns menu details
        """
        sql = sql_statement
        menu_list = []
        if  data is not None:
            menu_list = DbTransaction.retrieve_all(sql, data)
        else:
            menu_list = DbTransaction.retrieve_all(sql)

        _menu_ = []
        for menu_ in menu_list:
            menu_dict = {
                "item_id": menu_[0],
                "item_category": menu_[1],
                "item_name": menu_[2],
                "price": menu_[3]
            }
            print(menu_dict)
            _menu_.append(menu_dict)
        return jsonify({"message": "Available items on our menu",
                        "Menu": menu_})


    def post_menu_option(self, user_id):
        """
        This method adds menu options to the menu
        """
        keys = ("item_category", "item_name", "price")
        if not set(keys).issubset(set(request.json)):
            return self.error_message.request_missing_fields()

        request_condition = [
            request.json["item_category"].strip(),
            request.json["item_name"].strip(),
            request.json["price"]
            ]

        if not all(request_condition):
            return self.error_message.fields_missing_information(request.json)

        # user = DbTransaction.retrieve_one(
        #     """SELECT "user_id" FROM "users" WHERE "user_id" = %s""",
        #     (user_id, ))

        item_category = request.json['item_category']
        item_name = request.json['item_name']
        price = request.json['price']

        menu = Menu(item_category, item_name, price)
        menu.save_menu()
        return jsonify({"status_code": 201, "Menu": menu.get_menu_information(),
                        "message": "Menu option added successfully"}), 201

