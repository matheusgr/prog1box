#coding: utf-8
import webapp2
from google.appengine.api import memcache, users
from google.appengine.ext import ndb
from google.appengine.ext.webapp import template

from model import ExecScript, Network, AllowedUser
from utils import deny_access

DEBUG = False


class Dashboard(webapp2.RequestHandler):

    def get(self):
        if deny_access(self.response):
            return
        scripts = ExecScript.query()
        template_values = {
            'scripts': scripts,
        }
        path = 'dashboard.html'
        self.response.out.write(template.render(path, template_values))


class DashboardExecNew(webapp2.RequestHandler):
    def post(self):
        if deny_access(self.response):
            return
        code = '\n'.join(self.request.get('code').splitlines())
        name = self.request.get('name')
        network_name = self.request.get('network')
        network_key = Network.query(Network.name == network_name).get().key
        if not deny_access(self.response, network_key):
            ExecScript(code=code, name=name, network=network_key).put()
            self.redirect('/u/overview')
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
        self.redirect('/u/overview')


app = webapp2.WSGIApplication([
    ('/u/overview', Dashboard),
    ('/u/execedit', DashboardExecEdit),
    ('/u/execnew', DashboardExecNew),
], debug=DEBUG)
