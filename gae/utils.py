#coding: utf-8
from google.appengine.api import users
from model import AllowedUser


def deny_access(response, network_key=None):
    if not users.is_current_user_admin():
        user = users.get_current_user()
        if network_key:
            allowed_user = AllowedUser.query(AllowedUser.email == user.email() and AllowedUser.network == network_key).get()
        else:
            allowed_user = AllowedUser.query(AllowedUser.email == user.email()).get()
        if not allowed_user:
            response.set_status(403)
            response.out.write("You should have permission to access this page")
            return True
    return False
