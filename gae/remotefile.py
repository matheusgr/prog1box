import webapp2

from model import RemoteFile
import entity_controller

DEBUG = False


def _create_remote_file_attributes(self):
    return {"content": '\n'.join(self.request.get('content').splitlines()),
            "path": self.request.get('path')}


class RemoteFileNew(entity_controller.NewEntityController):
    entity = RemoteFile
    create_attributes = _create_remote_file_attributes


class RemoteFileEdit(entity_controller.EditEntityController):
    entity = RemoteFile
    create_attributes = _create_remote_file_attributes


app = webapp2.WSGIApplication([
    ('/t/remoteedit', RemoteFileEdit),
    ('/t/remotenew', RemoteFileNew),
], debug=DEBUG)
