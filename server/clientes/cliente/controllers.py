from .managers import *
from server.common.controllers import CrudController

import json


class ClienteController(CrudController):

    manager = ClienteManager
    html_index = "clientes/cliente/views/index.html"

    routes = {
        '/cliente': {'GET': 'index', 'POST': 'table'},
        '/cliente_insert': {'POST': 'insert'},
        '/cliente_update': {'PUT': 'edit', 'POST': 'update'},
        '/cliente_delete': {'POST': 'delete'}
    }


    def insert(self):
        self.set_session()
        diccionary = json.loads(self.get_argument("object"))
        diccionary['user'] = self.get_user_id()
        diccionary['ip'] = self.request.remote_ip
        ClienteManager(self.db).insert(diccionary)
        self.respond(success=True, message='Insertado correctamente.')

    def update(self):
        self.set_session()
        diccionary = json.loads(self.get_argument("object"))
        diccionary['user'] = self.get_user_id()
        diccionary['ip'] = self.request.remote_ip
        ClienteManager(self.db).update(diccionary)
        self.respond(success=True, message='Modificado correctamente.')


    def delete(self):
        self.set_session()
        diccionary = json.loads(self.get_argument("object"))

        id = diccionary['id']
        state = diccionary['enabled']
        respuesta = ClienteManager(self.db).delete(id, self.get_user_id(), self.request.remote_ip,state)

        self.respond(success=True, message=respuesta)
        self.db.close()
