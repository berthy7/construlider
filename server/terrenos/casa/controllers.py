from .managers import *
from server.common.controllers import CrudController

import json


class CasaController(CrudController):

    manager = CasaManager
    html_index = "terrenos/casa/views/index.html"
    routes = {
        '/casa': {'GET': 'index', 'POST': 'table'},
        '/casa_insert': {'POST': 'insert'},
        '/casa_update': {'PUT': 'edit', 'POST': 'update'},
        '/casa_delete': {'POST': 'delete'}
    }


    def insert(self):
        self.set_session()
        diccionary = json.loads(self.get_argument("object"))
        diccionary['user'] = self.get_user_id()
        diccionary['ip'] = self.request.remote_ip
        CasaManager(self.db).insert(diccionary)
        self.respond(success=True, message='Insertado correctamente.')

    def update(self):
        self.set_session()
        diccionary = json.loads(self.get_argument("object"))
        diccionary['user'] = self.get_user_id()
        diccionary['ip'] = self.request.remote_ip
        CasaManager(self.db).update(diccionary)
        self.respond(success=True, message='Modificado correctamente.')


    def delete(self):
        self.set_session()
        diccionary = json.loads(self.get_argument("object"))

        id = diccionary['id']
        state = diccionary['enabled']
        respuesta = CasaManager(self.db).delete(id, self.get_user_id(), self.request.remote_ip,state)

        self.respond(success=True, message=respuesta)
        self.db.close()
