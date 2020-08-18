from .managers import *
from server.common.controllers import CrudController

import json


class UrbanizacionController(CrudController):

    manager = UrbanizacionManager
    html_index = "terrenos/urbanizacion/views/index.html"
    html_table = "terrenos/urbanizacion/views/table.html"
    routes = {
        '/urbanizacion': {'GET': 'index', 'POST': 'table'},
        '/urbanizacion_insert': {'POST': 'insert'},
        '/urbanizacion_update': {'PUT': 'edit', 'POST': 'update'},
        '/urbanizacion_delete': {'POST': 'delete'}
    }


    def insert(self):
        self.set_session()
        diccionary = json.loads(self.get_argument("object"))
        diccionary['user'] = self.get_user_id()
        diccionary['ip'] = self.request.remote_ip
        UrbanizacionManager(self.db).insert(diccionary)
        self.respond(success=True, message='Insertado correctamente.')

    def update(self):
        self.set_session()
        diccionary = json.loads(self.get_argument("object"))
        diccionary['user'] = self.get_user_id()
        diccionary['ip'] = self.request.remote_ip
        UrbanizacionManager(self.db).update(diccionary)
        self.respond(success=True, message='Modificado correctamente.')


    def delete(self):
        self.set_session()
        diccionary = json.loads(self.get_argument("object"))

        id = diccionary['id']
        state = diccionary['enabled']
        respuesta = UrbanizacionManager(self.db).delete(id, self.get_user_id(), self.request.remote_ip,state)

        self.respond(success=True, message=respuesta)
        self.db.close()
