"""
This module is a menu model with its attributes
"""
from api.models.database_transaction import DbTransaction

class Order(object):
    """
    This class represents a order entity
    """

    def __init__(self, user_id, item_id, quantity):
        self.user_id = user_id
        self.item_id = item_id
        self.quantity = quantity
          
    def save_order(self):
        """
        This method saves order details
        """
        self.user_id
        self.item_id
        self.quantity
        
            
        order_sql = "INSERT INTO orders (user_id, item_id, quantity) VALUES\
        ('{}', '{}', '{}');".format(self.user_id, self.item_id, self.quantity)
        
        DbTransaction.save(order_sql)

    def get_order_information(self):
        """
        This method returns the information about an order.
        """

        return {
        "user_id":self.user_id,
        "item_id":self.item_id,
        "quantity": self.quantity
        }
