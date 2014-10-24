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

        machines = memcache.get('machines') or OrderedDict()
        remove_set = set()
        result = OrderedDict()
        networks = []

        for network in model.get_user_networks(user.email()):
            networks.append(netaddr.IPNetwork(network.addr))

        for ip, machine in machines.items():
            if machine.last_datetime < datetime.timedelta(minutes=-3) + datetime.datetime.now():
                remove_set.add(ip)
            else:
                for network in networks:
                    if netaddr.IPAddress(ip) in network:
                        result[ip] = machine
                        break

        for ip in remove_set:
            machines.pop(ip)

        memcache.set('machines', machines)

        template_values = {'is_admin': users.is_current_user_admin(), 'email': user.email(),
                           'logout': users.create_logout_url('/'), 'machines': result}
        template = jinja_environment.get_template('dashboard.html')
        self.response.out.write(template.render(template_values))

app = webapp2.WSGIApplication([
    ('/', Index),
    ('/exec', Exec),
], debug=DEBUG)
