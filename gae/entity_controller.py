import webapp2
from google.appengine.ext import ndb

from utils import deny_access
from model import invalidate_cache, RemoteFile, ExecScript


class NewEntityController(webapp2.RequestHandler):

    def post(self):
        if deny_access(self.response):
            return
        attributes = self.create_attributes()
        network_key_req = self.request.get('network')
        network_key = ndb.Key(urlsafe=network_key_req)
        if not deny_access(self.response, network_key):
            attributes['network'] = network_key
            self.entity(**attributes).put()
            invalidate_cache(network_key_req, self.entity)
            self.redirect('/')  # TODO AJAX
        else:
            self.response.set_status(403)


class EditEntityController(webapp2.RequestHandler):

    def post(self):
        if deny_access(self.response):
            return

        network_key = self.request.get('network')
        key = self.request.get('key')
        invalidate_cache(network_key, self.entity)

        if self.request.get('action') == "delete":
            ndb.Key(urlsafe=key).delete()
            self.redirect('/')  # TODO AJAX
            return

        # else: self.request.get('action') == "save"
        attributes = self.create_attributes()
        entity = ndb.Key(urlsafe=key).get()
        for attribute, value in attributes.items():
            setattr(entity, attribute, value)
        entity.put()
        self.redirect('/')  # TODO AJAX


def _create_remote_file_attributes(self):
    return {"content": '\n'.join(self.request.get('content').splitlines()),
            "path": self.request.get('path')}


def _create_script_attributes(self):
    return {"code": '\n'.join(self.request.get('code').splitlines()),
            "name": self.request.get('name')}


class RemoteFileNew(NewEntityController):
    entity = RemoteFile
    create_attributes = _create_remote_file_attributes


class RemoteFileEdit(EditEntityController):
    entity = RemoteFile
    create_attributes = _create_remote_file_attributes


class DashboardExecNew(NewEntityController):
    entity = ExecScript
    create_attributes = _create_script_attributes


class DashboardExecEdit(EditEntityController):
    entity = ExecScript
    create_attributes = _create_script_attributes


app = webapp2.WSGIApplication([
    ('/u/execedit', DashboardExecEdit),
    ('/u/execnew', DashboardExecNew),
    ('/t/remoteedit', RemoteFileEdit),
    ('/t/remotenew', RemoteFileNew),
], debug=False)