from .managers import *
from server.common.controllers import CrudController

import json


class EntidadController(CrudController):

    manager = EntidadManager
    html_index = "ventas/entidad/views/index.html"

    routes = {
        '/entidad': {'GET': 'index', 'POST': 'table'},
        '/entidad_insert': {'POST': 'insert'},
        '/entidad_update': {'PUT': 'edit', 'POST': 'update'},
        '/entidad_delete': {'POST': 'delete'}
    }


    def insert(self):
        self.set_session()
        dictionary = json.loads(self.get_argument("object"))
        dictionary['user'] = self.get_user_id()
        dictionary['ip'] = self.request.remote_ip
        EntidadManager(self.db).insert(dictionary)
        self.respond(success=True, message='Insertado correctamente.')

    def update(self):
        self.set_session()
        dictionary = json.loads(self.get_argument("object"))
        dictionary['user'] = self.get_user_id()
        dictionary['ip'] = self.request.remote_ip
        EntidadManager(self.db).update(dictionary)
        self.respond(success=True, message='Modificado correctamente.')


    def delete(self):
        self.set_session()
        dictionary = json.loads(self.get_argument("object"))

        id = dictionary['id']
        state = dictionary['enabled']
        respuesta = EntidadManager(self.db).delete(id, self.get_user_id(), self.request.remote_ip,state)

        self.respond(success=True, message=respuesta)
        self.db.close()
