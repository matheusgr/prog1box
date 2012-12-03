#coding: utf-8

import datetime

import webapp2
from google.appengine.api import memcache
from google.appengine.ext import db
from google.appengine.api import users
from google.appengine.ext.webapp import template


DEBUG = False

class ExecScript(db.Model):
    code = db.TextProperty(required=True)
    name = db.StringProperty(required=True)

class AllowedUser(db.Model):
    email = db.StringProperty(required=True)


def deny_access(response):
    if not users.is_current_user_admin():
        user = users.get_current_user()
        allowed_user = AllowedUser.all().filter('email =', user.email()).get()
        if not allowed_user:
            response.set_status(403)
            response.out.write("You should have permission to access this page")
            return True
    return False


class Exec(webapp2.RequestHandler):
    def get(self):
        machines_dict = memcache.get('machines') or {}
        last_exec = self.request.get('last', default_value = '-1')
        machine_id = self.request.get('id', default_value= '')
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
  ('/admin', Admin),
  ('/admin/user', AdminUser),
  ('/admin/useredit', AdminUserEdit),
  ('/admin/usernew', AdminUserNew),
  ('/admin/execedit', AdminExecEdit),
  ('/admin/execnew', AdminExecNew),
  ], debug=DEBUG)

