import webapp2

import entity_controller
from model import ExecScript

DEBUG = False


def _create_script_attributes(self):
    return {"code": '\n'.join(self.request.get('code').splitlines()),
            "name": self.request.get('name')}


class DashboardExecNew(entity_controller.NewEntityController):
    entity = ExecScript
    create_attributes = _create_script_attributes


class DashboardExecEdit(entity_controller.EditEntityController):
    entity = ExecScript
    create_attributes = _create_script_attributes


app = webapp2.WSGIApplication([
    ('/u/execedit', DashboardExecEdit),
    ('/u/execnew', DashboardExecNew),
], debug=DEBUG)
