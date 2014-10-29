import webapp2
from google.appengine.ext import ndb

from utils import deny_access
from model import RemoteFile

DEBUG = False


class RemoteFileNew(webapp2.RequestHandler):
    def post(self):
        if deny_access(self.response):
            return
        content = '\n'.join(self.request.get('content').splitlines())
        path = self.request.get('path')
        network_key = ndb.Key(urlsafe=self.request.get('network'))
        if not deny_access(self.response, network_key):
            RemoteFile(content=content, path=path, network=network_key).put()
            self.redirect('/')  # TODO AJAX
        else:
            self.response.set_status(403)


class RemoteFileEdit(webapp2.RequestHandler):
    def post(self):
        if deny_access(self.response):
            return
        path = self.request.get('path')
        content = '\n'.join(self.request.get('content').splitlines())
        key = self.request.get('key')
        r_file = ndb.Key(urlsafe=key).get()
        r_file.path = path
        r_file.content = content
        r_file.put()
        self.redirect('/')  # TODO AJAX


app = webapp2.WSGIApplication([
    ('/t/remoteedit', RemoteFileEdit),
    ('/t/remotenew', RemoteFileNew),
], debug=DEBUG)
