from .managers import *
from server.common.controllers import CrudController

import json


class ReservaController(CrudController):

    manager = ReservaManager
    html_index = "ventas/reserva/views/index.html"

    routes = {
        '/reserva': {'GET': 'index', 'POST': 'table'},
        '/reserva_insert': {'POST': 'insert'},
        '/reserva_update': {'PUT': 'edit', 'POST': 'update'},
        '/reserva_delete': {'POST': 'delete'}
    }

    def get_extra_data(self):
        aux = super().get_extra_data()

        return aux


    def insert(self):
        self.set_session()
        diccionary = json.loads(self.get_argument("object"))
        diccionary['user'] = self.get_user_id()
        diccionary['ip'] = self.request.remote_ip
        ReservaManager(self.db).insert(diccionary)
        self.respond(success=True, message='Insertado correctamente.')

    def update(self):
        self.set_session()
        diccionary = json.loads(self.get_argument("object"))
        diccionary['user'] = self.get_user_id()
        diccionary['ip'] = self.request.remote_ip
        ReservaManager(self.db).update(diccionary)
        self.respond(success=True, message='Modificado correctamente.')


    def delete(self):
        self.set_session()
        diccionary = json.loads(self.get_argument("object"))

        id = diccionary['id']
        state = diccionary['enabled']
        respuesta = ReservaManager(self.db).delete(id, self.get_user_id(), self.request.remote_ip,state)

        self.respond(success=True, message=respuesta)
        self.db.close()
