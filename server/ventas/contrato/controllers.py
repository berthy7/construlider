from .managers import *
from server.common.controllers import CrudController

import json


class ContratoController(CrudController):

    manager = ContratoManager
    html_index = "ventas/contrato/views/index.html"
    html_table = "ventas/contrato/views/table.html"
    routes = {
        '/contrato': {'GET': 'index', 'POST': 'table'},
        '/contrato_insert': {'POST': 'insert'},
        '/contrato_update': {'PUT': 'edit', 'POST': 'update'},
        '/contrato_delete': {'POST': 'delete'}
    }


    def insert(self):
        self.set_session()
        diccionary = json.loads(self.get_argument("object"))
        diccionary['user'] = self.get_user_id()
        diccionary['ip'] = self.request.remote_ip
        ContratoManager(self.db).insert(diccionary)
        self.respond(success=True, message='Insertado correctamente.')

    def update(self):
        self.set_session()
        diccionary = json.loads(self.get_argument("object"))
        diccionary['user'] = self.get_user_id()
        diccionary['ip'] = self.request.remote_ip
        ContratoManager(self.db).update(diccionary)
        self.respond(success=True, message='Modificado correctamente.')


    def delete(self):
        self.set_session()
        diccionary = json.loads(self.get_argument("object"))

        id = diccionary['id']
        state = diccionary['enabled']
        respuesta = ContratoManager(self.db).delete(id, self.get_user_id(), self.request.remote_ip,state)

        self.respond(success=True, message=respuesta)
        self.db.close()
