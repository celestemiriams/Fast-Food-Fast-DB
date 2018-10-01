"""
This module is a menu model with its attributes
"""
from api.models.database_transaction import DbTransaction

class Menu(object):
    """
    This class represents a menu entity
    """

    def __init__(self, *args):
        self.item_category = args[0]
        self.item_name = args[1]
        self.price = args[2]
        
    
    def save_menu(self):
        """
        This method saves menu options
        """
        self.item_category
        self.item_name
        self.price 
            
        menu_sql = "INSERT INTO menu (item_category, item_name, price) VALUES\
        ('{}', '{}', '{}');".format(self.item_category, self.item_name, self.price)
        
        DbTransaction.save(menu_sql)

    def get_menu_information(self):
        """
        This method returns the information about a menu.
        """

        return {
            "item_category": self.item_category,
            "item_name": self.item_name,
            "price": self.price
        }
