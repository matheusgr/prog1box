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

class Admin(webapp2.RequestHandler):
    def get(self):
        scripts = ExecScript.all()
        template_values = {
            'scripts': scripts,
        }
        path = 'admin.html'
        self.response.out.write(template.render(path, template_values))

class AdminExecNew(webapp2.RequestHandler):
    def post(self):
        code = '\n'.join(self.request.get('code').splitlines())
        name = self.request.get('name')
        ExecScript(code=code, name=name).put()
        self.redirect('/admin')

class AdminExecEdit(webapp2.RequestHandler):
    def post(self):
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
        self.response.out.write('Online...<br><br>')
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
  ('/admin/execedit', AdminExecEdit),
  ('/admin/execnew', AdminExecNew),
  ], debug=DEBUG)

