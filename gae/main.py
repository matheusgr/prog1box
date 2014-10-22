#coding: utf-8

import datetime

import webapp2
from google.appengine.api import memcache
from google.appengine.api import users

from model import ExecScript
from utils import deny_access

DEBUG = False


class Exec(webapp2.RequestHandler):
    def get(self):
        machines_dict = memcache.get('machines') or {}
        last_exec = self.request.get('last', default_value='-1')
        machine_ip = self.request.remote_addr
        machines_dict[machine_ip] = (datetime.datetime.now(), last_exec)
        memcache.set('machines', machines_dict)
        data = memcache.get('execdefault')
        if data is not None:
            script = data
        else:
            script = ExecScript.all().filter('name =', 'default').get().code
            memcache.set('execdefault', script)
        self.response.headers['Content-Type'] = 'text/plain'
        self.response.out.write(script)


class Index(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()
        if not user:
            self.response.out.write("<a href=%s>Login</a><br><br>" % users.create_login_url())
            return
        else:
            if deny_access(self.response):
                self.response.out.write("<br><br>User %s - <a href=%s>Logout</a><br>" % (user.email(), users.create_logout_url('/')))
                return
            self.response.out.write("User %s - <a href=%s>Logout</a><br>" % (user.email(), users.create_logout_url('/')))
            self.response.out.write("<a href=/admin>Edit exec script</a><br>")
            self.response.out.write("<a href=/admin/user>Edit allowed users</a><br><br>")
        machines_dict = memcache.get('machines')
        if not machines_dict:
            self.response.out.write('None')
            return
        machines = machines_dict.items()
        machines.sort(key=lambda x: x[0])
        for machine in machines:
            if machine[1][0] < datetime.timedelta(minutes=-3) + datetime.datetime.now():
                del machines_dict[machine[0]]
            else:
                self.response.out.write('%s : %s : %s<br>' % (machine[0], machine[1][0], machine[1][1]))
        self.response.out.write('---')
        memcache.set('machines', machines_dict)


app = webapp2.WSGIApplication([
    ('/', Index),
    ('/exec', Exec),
], debug=DEBUG)
