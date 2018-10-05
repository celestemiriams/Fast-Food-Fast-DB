"""
This module handles requests to urls.
"""
from api.controller.menu_view import MenuViews
from api.controller.order_view import OrderViews
from api.controller.user_view import UserViews
from api.auth.auth_view import RegisterUser, LoginUser, Logout


class Urls(object):
    """
    Class to generate urls
    """
    @staticmethod
    def generate_url(app):
        """
         Generates urls on the app context
        """
        menu_view = MenuViews.as_view('menu_api')
        order_view = OrderViews.as_view('order_api')
        user_view = UserViews.as_view('user_api')
        app.add_url_rule('/api/v1/auth/signup/', view_func=RegisterUser.as_view('register_user'),
                         methods=["POST",])
        app.add_url_rule('/api/v1/auth/login/', view_func=LoginUser.as_view('login_user'),
                         methods=["POST",])
        app.add_url_rule('/api/v1/users/logout',
                         view_func=Logout.as_view('logout_user'),
                         methods=["POST",])
        app.add_url_rule('/api/v1/menu/', view_func=menu_view,
                         methods=["GET", 'POST'])
        app.add_url_rule('/api/v1/orders/', defaults={'order_id':None},
                         view_func=order_view, methods=["GET",])
        app.add_url_rule('/api/v1/orders/<int:order_id>/', view_func=order_view,
                         methods=["GET",])
        app.add_url_rule('/api/v1/users/orders/', view_func=order_view,
                         methods=["POST",])
        app.add_url_rule('/api/v1/users/orders/', view_func=user_view,
                         methods=["GET",])
        app.add_url_rule('/api/v1/orders/<int:order_id>/', view_func=order_view,
                         methods=["PUT",])
        
                

        