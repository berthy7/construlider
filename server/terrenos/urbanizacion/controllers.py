from .managers import *
from server.common.controllers import CrudController
from server.parametros.moneda.managers import *

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

    def get_extra_data(self):
        aux = super().get_extra_data()

        aux['monedas'] = MonedaManager(self.db).listar_todo()

        return aux


    def insert(self):
        self.set_session()
        dictionary = json.loads(self.get_argument("object"))
        dictionary['user'] = self.get_user_id()
        dictionary['ip'] = self.request.remote_ip
        UrbanizacionManager(self.db).insert(dictionary)
        self.respond(success=True, message='Insertado correctamente.')

    def update(self):
        self.set_session()
        dictionary = json.loads(self.get_argument("object"))
        dictionary['user'] = self.get_user_id()
        dictionary['ip'] = self.request.remote_ip
        UrbanizacionManager(self.db).update(dictionary)
        self.respond(success=True, message='Modificado correctamente.')


    def delete(self):
        self.set_session()
        dictionary = json.loads(self.get_argument("object"))

        id = dictionary['id']
        state = dictionary['enabled']
        respuesta = UrbanizacionManager(self.db).delete(id, self.get_user_id(), self.request.remote_ip,state)

        self.respond(success=True, message=respuesta)
        self.db.close()
