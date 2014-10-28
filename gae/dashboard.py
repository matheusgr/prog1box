#coding: utf-8
import webapp2
from google.appengine.api import memcache, users
from google.appengine.ext import ndb
from google.appengine.ext.webapp import template

from model import ExecScript, Network, AllowedUser
from utils import deny_access

DEBUG = False


class DashboardExecNew(webapp2.RequestHandler):
    def post(self):
        if deny_access(self.response):
            return
        code = '\n'.join(self.request.get('code').splitlines())
        name = self.request.get('name')
        network_key = ndb.Key(urlsafe=self.request.get('network'))
        if not deny_access(self.response, network_key):
            ExecScript(code=code, name=name, network=network_key).put()
            self.redirect('/')  # TODO AJAX
        else:
            self.response.set_status(403)


class DashboardExecEdit(webapp2.RequestHandler):
    def post(self):
        if deny_access(self.response):
            return
        name = self.request.get('name')
        code = '\n'.join(self.request.get('code').splitlines())
        key = self.request.get('key')
        script = ndb.Key(urlsafe=key).get()
        script.name = name
        script.code = code
        script.put()
        if name == 'default':
            memcache.set('execdefault', code)
        self.redirect('/')  # TODO AJAX


app = webapp2.WSGIApplication([
    ('/u/execedit', DashboardExecEdit),
    ('/u/execnew', DashboardExecNew),
], debug=DEBUG)
