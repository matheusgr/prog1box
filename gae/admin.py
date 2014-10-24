#coding: utf-8
import webapp2
from google.appengine.ext import db
from google.appengine.ext.webapp import template

from model import AllowedUser


DEBUG = False


class AdminUser(webapp2.RequestHandler):

    def get(self):
        allowed_users = AllowedUser.query().order(AllowedUser.email)
        template_values = {
            'users': allowed_users,
        }
        path = 'admin.html'
        self.response.out.write(template.render(path, template_values))


class AdminUserNew(webapp2.RequestHandler):

    def post(self):
        email = self.request.get('email')
        AllowedUser(email=email).put()
        self.redirect('/admin/user')


class AdminUserEdit(webapp2.RequestHandler):

    def post(self):
        key = self.request.get('key')
        db.delete(key)
        self.redirect('/admin/user')


app = webapp2.WSGIApplication([
    ('/admin/user', AdminUser),
    ('/admin/useredit', AdminUserEdit),
    ('/admin/usernew', AdminUserNew),
], debug=DEBUG)
