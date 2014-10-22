#coding: utf-8
import webapp2
from google.appengine.api import memcache
from google.appengine.ext import db
from google.appengine.ext.webapp import template

from model import ExecScript, AllowedUser
from utils import deny_access


DEBUG = False


class AdminUser(webapp2.RequestHandler):

    def get(self):
        allowed_users = AllowedUser.all().order('email')
        template_values = {
            'users': allowed_users,
        }
        path = 'users.html'
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


class Admin(webapp2.RequestHandler):

    def get(self):
        if deny_access(self.response):
            return
        scripts = ExecScript.all()
        template_values = {
            'scripts': scripts,
        }
        path = 'admin.html'
        self.response.out.write(template.render(path, template_values))


class AdminExecNew(webapp2.RequestHandler):
    def post(self):
        if deny_access(self.response):
            return
        code = '\n'.join(self.request.get('code').splitlines())
        name = self.request.get('name')
        ExecScript(code=code, name=name).put()
        self.redirect('/admin')


class AdminExecEdit(webapp2.RequestHandler):
    def post(self):
        if deny_access(self.response):
            return
        name = self.request.get('name')
        code = '\n'.join(self.request.get('code').splitlines())
        key = self.request.get('key')
        script = db.get(key)
        script.name = name
        script.code = code
        script.put()
        if name == 'default':
            memcache.set('execdefault', code)
        self.redirect('/admin')


app = webapp2.WSGIApplication([
    ('/admin', Admin),
    ('/admin/user', AdminUser),
    ('/admin/useredit', AdminUserEdit),
    ('/admin/usernew', AdminUserNew),
    ('/admin/execedit', AdminExecEdit),
    ('/admin/execnew', AdminExecNew),
], debug=DEBUG)
