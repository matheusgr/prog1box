#coding: utf-8
import webapp2
from google.appengine.api import memcache
from google.appengine.ext import db
from google.appengine.ext.webapp import template

from model import ExecScript
from utils import deny_access

DEBUG = False


class Admin(webapp2.RequestHandler):

    def get(self):
        if deny_access(self.response):
            return
        scripts = ExecScript.query()
        template_values = {
            'scripts': scripts,
        }
        path = 'dashboard.html'
        self.response.out.write(template.render(path, template_values))


class AdminExecNew(webapp2.RequestHandler):
    def post(self):
        if deny_access(self.response):
            return
        code = '\n'.join(self.request.get('code').splitlines())
        name = self.request.get('name')
        ExecScript(code=code, name=name).put()
        self.redirect('/u/overview')


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
        self.redirect('/u/overview')


app = webapp2.WSGIApplication([
    ('/u/overview', Admin),
    ('/u/execedit', AdminExecEdit),
    ('/u/execnew', AdminExecNew),
], debug=DEBUG)
