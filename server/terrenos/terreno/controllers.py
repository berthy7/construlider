from .managers import *
from server.common.controllers import CrudController
from server.terrenos.urbanizacion.managers import *

import json


class TerrenoController(CrudController):

    manager = TerrenoManager
    html_index = "terrenos/terreno/views/index.html"
    html_table = "terrenos/terreno/views/table.html"
    routes = {
        '/terreno': {'GET': 'index', 'POST': 'table'},
        '/terreno_insert': {'POST': 'insert'},
        '/terreno_update': {'PUT': 'edit', 'POST': 'update'},
        '/terreno_delete': {'POST': 'delete'}
    }

    def get_extra_data(self):
        aux = super().get_extra_data()
        aux['urbanizaciones'] = UrbanizacionManager(self.db).listar_habilitados()

        return aux


    def insert(self):
        self.set_session()
        diccionary = json.loads(self.get_argument("object"))
        diccionary['user'] = self.get_user_id()
        diccionary['ip'] = self.request.remote_ip
        TerrenoManager(self.db).insert(diccionary)
        self.respond(success=True, message='Insertado correctamente.')

    def update(self):
        self.set_session()
        diccionary = json.loads(self.get_argument("object"))
        diccionary['user'] = self.get_user_id()
        diccionary['ip'] = self.request.remote_ip
        TerrenoManager(self.db).update(diccionary)
        self.respond(success=True, message='Modificado correctamente.')


    def delete(self):
        self.set_session()
        diccionary = json.loads(self.get_argument("object"))

        id = diccionary['id']
        state = diccionary['enabled']
        respuesta = TerrenoManager(self.db).delete(id, self.get_user_id(), self.request.remote_ip,state)

        self.respond(success=True, message=respuesta)
        self.db.close()
