#coding: utf-8
import datetime
import os
from collections import OrderedDict

import webapp2
from google.appengine.api import memcache
from google.appengine.api import users
import jinja2

import netaddr
import model
from utils import deny_access


DEBUG = False

jinja_environment = jinja2.Environment(autoescape=True,
                                       loader=jinja2.FileSystemLoader(
                                           os.path.join(os.path.dirname(__file__), 'bootstrap')))


class Machine:
    def __init__(self, last_datetime, last_output):
        self.last_datetime = last_datetime
        self.last_output = last_output

    def __cmp__(self, other):
        return cmp(self.ip, other.ip)


class Exec(webapp2.RequestHandler):
    def get(self):
        machines_dict = memcache.get('machines') or OrderedDict()
        last_exec = self.request.get('last', default_value='-1')
        machine_ip = self.request.remote_addr
        machines_dict[machine_ip] = Machine(datetime.datetime.now(), last_exec)
        memcache.set('machines', machines_dict)
        script = model.get_default_script(machine_ip)
        self.response.headers['Content-Type'] = 'text/plain'
        self.response.out.write(script)


class Index(webapp2.RequestHandler):

    @staticmethod
    def _get_user_machines(user_email):

        machines = memcache.get('machines') or OrderedDict()
        result = {}
        total_users_machines = 0
        networks_model = model.get_user_networks(user_email, users.is_current_user_admin())

        for ip, machine in list(machines.items()):
            if machine.last_datetime < datetime.timedelta(minutes=-3) + datetime.datetime.now():
                machines.pop(ip)
            else:
                for network in networks_model:
                    if netaddr.IPAddress(ip) in network.netaddr:
                        result_dict = result.get(network.name, OrderedDict())
                        result_dict[ip] = machine
                        result[network.name] = result_dict
                        total_users_machines += 1
                        break

        memcache.set('machines', machines)

        return networks_model, result, total_users_machines

    def get(self):
        user = users.get_current_user()

        if not user:
            template_values = {'login': users.create_login_url()}
            template = jinja_environment.get_template('index.html')
            self.response.out.write(template.render(template_values))
            return

        if deny_access(self.response):
            self.response.set_status(403)
            self.response.out.write("<br><br>User %s - <a href=%s>Logout</a><br>" %
                                    (user.email(), users.create_logout_url('/')))
            return

        networks_model, result, total_users_machines = self._get_user_machines(user.email())

        template_values = {'is_admin': users.is_current_user_admin(),
                           'nick': user.nickname(),
                           'email': user.email(),
                           'total_users_machines': total_users_machines,
                           'logout': users.create_logout_url('/'),
                           'machines': result,
                           'networks': networks_model}
        template = jinja_environment.get_template('dashboard.html')
        self.response.out.write(template.render(template_values))

app = webapp2.WSGIApplication([
    ('/', Index),
    ('/exec', Exec),
], debug=DEBUG)
