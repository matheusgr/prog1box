import webapp2
from google.appengine.ext import ndb
from google.appengine.ext.webapp import template

from model import AllowedUser, Network, flush_cache


DEBUG = False


class AdminUser(webapp2.RequestHandler):
    def get(self):
        allowed_users = AllowedUser.query().order(AllowedUser.email)
        networks = Network.query().order(Network.name)
        template_values = {
            'users': allowed_users,
            'networks': networks
        }
        path = 'admin.html'
        self.response.out.write(template.render(path, template_values))


class AdminUserNew(webapp2.RequestHandler):
    def post(self):
        email = self.request.get('email')
        network_name = self.request.get('network')
        network_key = Network.query(Network.name == network_name).get().key
        AllowedUser(email=email, network=network_key).put()
        self.redirect('/admin/user')


class AdminUserEdit(webapp2.RequestHandler):
    def post(self):
        key = self.request.get('key')
        ndb.Key(urlsafe=key).delete()
        self.redirect('/admin/user')


class AdminNetworkNew(webapp2.RequestHandler):
    def post(self):
        name = self.request.get('name')
        addr = self.request.get('addr')
        Network(name=name, addr=addr).put()
        flush_cache()
        self.redirect('/admin/user')


class AdminNetworkEdit(webapp2.RequestHandler):
    def post(self):
        key = self.request.get('key')
        ndb.Key(urlsafe=key).delete()
        flush_cache()
        self.redirect('/admin/user')


app = webapp2.WSGIApplication([
                                  ('/admin/user', AdminUser),
                                  ('/admin/useredit', AdminUserEdit),
                                  ('/admin/usernew', AdminUserNew),
                                  ('/admin/networkedit', AdminNetworkEdit),
                                  ('/admin/networknew', AdminNetworkNew),
                              ], debug=DEBUG)
