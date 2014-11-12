import webapp2
from google.appengine.ext import ndb

from utils import deny_access
from model import ExecScript, invalidate_cache

DEBUG = False


class DashboardExecNew(webapp2.RequestHandler):
    def post(self):
        if deny_access(self.response):
            return
        code = '\n'.join(self.request.get('code').splitlines())
        name = self.request.get('name')
        network_key_req = self.request.get('network')
        network_key = ndb.Key(urlsafe=network_key_req)
        if not deny_access(self.response, network_key):
            ExecScript(code=code, name=name, network=network_key).put()
            invalidate_cache(network_key_req, ExecScript)
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
        network_key = self.request.get('network')
        script = ndb.Key(urlsafe=key).get()
        script.name = name
        script.code = code
        script.put()
        invalidate_cache(network_key, ExecScript)
        self.redirect('/')  # TODO AJAX


app = webapp2.WSGIApplication([
    ('/u/execedit', DashboardExecEdit),
    ('/u/execnew', DashboardExecNew),
], debug=DEBUG)
