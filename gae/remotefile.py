import webapp2
from google.appengine.ext import ndb

from utils import deny_access
from model import RemoteFile, invalidate_cache

DEBUG = False


class RemoteFileNew(webapp2.RequestHandler):
    def post(self):
        if deny_access(self.response):
            return
        content = '\n'.join(self.request.get('content').splitlines())
        path = self.request.get('path')
        network_key_req = self.request.get('network')
        network_key = ndb.Key(urlsafe=network_key_req)
        if not deny_access(self.response, network_key):
            RemoteFile(content=content, path=path, network=network_key).put()
            invalidate_cache(network_key_req, RemoteFile)
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
        network_key = self.request.get('network')
        r_file = ndb.Key(urlsafe=key).get()
        r_file.path = path
        r_file.content = content
        r_file.put()
        invalidate_cache(network_key, RemoteFile)
        self.redirect('/')  # TODO AJAX


app = webapp2.WSGIApplication([
    ('/t/remoteedit', RemoteFileEdit),
    ('/t/remotenew', RemoteFileNew),
], debug=DEBUG)
