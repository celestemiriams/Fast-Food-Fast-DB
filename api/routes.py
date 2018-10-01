"""
This module handles requests to urls.
"""
from api.views.menu_view import MenuViews
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
        app.add_url_rule('/api/v1/auth/signup/', view_func=RegisterUser.as_view('register_user'),
                         methods=["POST",])
        app.add_url_rule('/api/v1/auth/login/', view_func=LoginUser.as_view('login_user'),
                         methods=["POST",])
        app.add_url_rule('/api/v1/users/logout',
                         view_func=Logout.as_view('logout_user'),
                         methods=["POST",])
        app.add_url_rule('/api/v1/menu/', view_func=menu_view,
                         methods=['GET', 'POST'])

        